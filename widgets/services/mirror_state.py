from django.core.cache import cache

class MirrorStateService:
    @staticmethod
    def get_state():
        state = cache.get("mirror_current_state")
        if not state:
            return {"status": "standby"}
        return state

    @staticmethod
    def set_state(state_dict):
        # timeout=86400 (1 dia) para não expirar rápido.
        # Isso atua como o "Cérebro Central" do espelho.
        cache.set("mirror_current_state", state_dict, 86400)
