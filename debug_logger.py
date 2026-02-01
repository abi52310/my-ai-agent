DEBUG_MODE = True   # ⭐ Turn OFF by making False


def debug_log(component, message):

    if DEBUG_MODE:
        print(f"[DEBUG][{component}] {message}")
