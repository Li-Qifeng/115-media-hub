import logging
import re
import threading
import time

import requests

from .base import CloudProvider
from .registry import register


class AliyunProvider(CloudProvider):
    name = "aliyun"
    label = "阿里云盘"
    link_type = "aliyun"
    auth_type = "refresh_token"
    config_keys = ["aliyun_refresh_token"]
    supports_offline = False
    supports_fixed_share_link = False

    def __init__(self):
        super().__init__()
        self._access_token = None
        self._token_expiry = 0.0
        self._token_lock = threading.Lock()

    def _ensure_access_token(self, refresh_token: str) -> str:
        now = time.time()
        with self._token_lock:
            if self._access_token and now < self._token_expiry - 60:
                return self._access_token
            resp = requests.post(
                "https://auth.aliyundrive.com/v2/account/token",
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            token = data.get("access_token")
            if not token:
                raise RuntimeError("阿里云盘 access_token 获取失败，请检查 refresh_token 是否有效")
            self._access_token = token
            self._token_expiry = now + int(data.get("expires_in", 7200))
            return token

    def _api_headers(self, refresh_token: str) -> dict:
        token = self._ensure_access_token(refresh_token)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

    def _api_post(self, refresh_token: str, url: str, body: dict, timeout: int = 30) -> dict:
        self.throttle()
        resp = requests.post(
            url,
            headers=self._api_headers(refresh_token),
            json=body,
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") and str(data["code"]).strip() not in ("", "Success"):
            raise RuntimeError(f"阿里云盘 API 错误: {data.get('message', '未知错误')}")
        return data

    def _resolve_drive_id(self, refresh_token: str) -> str:
        data = self._api_post(refresh_token, "https://api.aliyundrive.com/v2/user/get", {})
        return data.get("default_drive_id", "")

    def list_entries_payload(self, cookie, cid="root", folders_only=False):
        body = {
            "drive_id": self._resolve_drive_id(refresh_token=cookie),
            "parent_file_id": cid or "root",
            "limit": 200,
            "order_by": "updated_at",
            "order_direction": "DESC",
        }
        if folders_only:
            body["type"] = "folder"
        data = self._api_post(cookie, "https://api.aliyundrive.com/v2/file/list", body)
        entries = []
        for item in data.get("items", []):
            entries.append({
                "id": str(item.get("file_id", "")),
                "name": str(item.get("name", "")),
                "type": "folder" if item.get("type") == "folder" else "file",
                "size": int(item.get("size", 0) or 0),
                "parent_id": str(item.get("parent_file_id", cid)),
            })
        return {"entries": entries, "total": len(entries)}

    def list_entries(self, cookie, cid="root"):
        return self.list_entries_payload(cookie, cid)["entries"]

    def create_folder(self, cookie, cid="root", folder_name=""):
        data = self._api_post(cookie, "https://api.aliyundrive.com/v2/file/create", {
            "drive_id": self._resolve_drive_id(refresh_token=cookie),
            "parent_file_id": cid or "root",
            "name": folder_name,
            "type": "folder",
            "check_name_mode": "refuse",
        })
        return {"cid": str(data.get("file_id", "")), "name": folder_name}

    def resolve_folder_id_by_path(self, cookie, relative_path):
        parts = [p.strip() for p in str(relative_path).split("/") if p.strip()]
        cid = "root"
        for name in parts:
            entries = self.list_entries(cookie, cid)
            found = next((e for e in entries if e.get("name") == name), None)
            if not found:
                return ""
            cid = found["id"]
        return cid

    def ensure_folder_id_by_path(self, cookie, relative_path):
        parts = [p.strip() for p in str(relative_path).split("/") if p.strip()]
        cid = "root"
        for name in parts:
            entries = self.list_entries(cookie, cid)
            found = next((e for e in entries if e.get("name") == name), None)
            if found:
                cid = found["id"]
            else:
                result = self.create_folder(cookie, cid, name)
                cid = result["cid"]
        return cid

    def resolve_share_payload(self, cookie, share_url, raw_text="", receive_code=""):
        share_id_match = re.search(r'/s/([A-Za-z0-9]+)', str(share_url))
        if not share_id_match:
            raise RuntimeError("无法识别阿里云盘分享链接")
        return {
            "share_id": share_id_match.group(1),
            "receive_code": str(receive_code or "").strip(),
        }

    def list_share_entries(self, cookie, share_payload, cid="root", offset=0, limit=200):
        share_id = share_payload["share_id"]
        receive_code = share_payload.get("receive_code", "")

        data = self._api_post(cookie, "https://api.aliyundrive.com/v2/share_link/get_share_by_anonymous", {
            "share_id": share_id,
        })
        share_token = data.get("share_token", "")

        if receive_code:
            self._api_post(cookie, "https://api.aliyundrive.com/v2/share_link/verify_code", {
                "share_id": share_id,
                "share_pwd": receive_code,
            })

        entries_data = self._api_post(cookie, "https://api.aliyundrive.com/v2/file/list_share", {
            "share_id": share_id,
            "parent_file_id": cid or "root",
            "limit": limit,
            "share_token": share_token,
        })
        entries = []
        for item in entries_data.get("items", []):
            entries.append({
                "id": str(item.get("file_id", "")),
                "name": str(item.get("name", "")),
                "type": "folder" if item.get("type") == "folder" else "file",
                "size": int(item.get("size", 0) or 0),
                "share_id": share_id,
                "share_token": share_token,
            })
        return {
            "entries": entries,
            "total": len(entries),
            "share": {**share_payload, "share_token": share_token},
        }

    def prepare_share_receive(self, cookie, share_payload, cid="root"):
        return {**share_payload, "target_cid": cid or "root"}

    def submit_share_receive(self, cookie, receive_payload, files):
        share_id = receive_payload["share_id"]
        share_token = receive_payload.get("share_token", "")
        target_cid = receive_payload.get("target_cid", "root")
        drive_id = self._resolve_drive_id(refresh_token=cookie)

        file_ids = [
            str(f.get("id", "")).strip()
            for f in (files or [])
            if str(f.get("id", "")).strip()
        ]
        if not file_ids:
            raise RuntimeError("未选择要转存的文件")

        for fid in file_ids:
            self._api_post(cookie, "https://api.aliyundrive.com/v2/file/copy", {
                "drive_id": drive_id,
                "file_id": fid,
                "to_parent_file_id": target_cid,
                "share_id": share_id,
                "share_token": share_token,
            }, timeout=60)

        return {"success": True, "count": len(file_ids)}

    def probe_connectivity(self, cookie):
        try:
            self._ensure_access_token(cookie)
            return True
        except Exception as e:
            logging.warning(f"阿里云盘连接检测失败: {e}")
            return False


register(AliyunProvider())
