#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Predictor.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1 and 'runserver' in sys.argv:
        import socket
        try:
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
        local_ip = "127.0.0.1"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
            except Exception:
                pass
        print("=" * 65)
        print("🚀 CLINICAL AI DIABETES PREDICTION SERVER IS ONLINE!")
        print(f"💻 Local Access: http://127.0.0.1:8000")
        print(f"🌐 LAN/Wi-Fi Access (For other devices): http://{local_ip}:8000")
        print("=" * 65)
        print()
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
