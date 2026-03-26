"""
gen_memurai_conf.py — Genera memurai.conf con rutas Windows correctas
BookingScraper Pro v6.0.0 | Windows 11

FIX-MEMURAI-005: reemplaza la generación anterior con sed que producía
  dobles backslashes (C:\\\\BookingScraper\\\\) en logfile y dir.
  Python maneja las rutas con pathlib — sin escapes incorrectos.

Uso:
  python scripts/gen_memurai_conf.py
  python scripts/gen_memurai_conf.py --base "D:\\MiProyecto"

La ruta base se detecta automáticamente como el directorio padre de
este script (es decir: BASE_DIR == C:\\BookingScraper).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _win_path(p: Path) -> str:
    """
    Convierte un Path de Windows a cadena con barras invertidas simples.
    Redis/Memurai en Windows acepta rutas con '\' o '/' — usamos '/' para
    evitar cualquier problema de interpretación en el archivo .conf.
    """
    return str(p).replace("\\", "/")


def generate(base_dir: Path) -> str:
    """
    Genera el contenido de memurai.conf para el directorio base dado.
    Solo se incluyen directivas esenciales para BookingScraper Pro.
    """
    logs_dir  = base_dir / "logs"
    log_file  = logs_dir / "memurai.log"

    # Asegurar que el directorio de logs existe
    logs_dir.mkdir(parents=True, exist_ok=True)

    conf = f"""\
# memurai.conf — BookingScraper Pro v6.0.0
# Generado automáticamente por scripts/gen_memurai_conf.py
# NO editar manualmente — ejecuta gen_memurai_conf.py para regenerar.
#
# Memurai Developer Edition — compatible con Redis 5.x API
# Docs: https://docs.memurai.com/

# ── Red ──────────────────────────────────────────────────────────────────────
bind 127.0.0.1
port 6379
protected-mode yes

# ── Base de datos y directorios ──────────────────────────────────────────────
# FIX-MEMURAI-005: rutas generadas con pathlib — sin dobles backslashes.
dir {_win_path(base_dir)}

# ── Logging ──────────────────────────────────────────────────────────────────
loglevel notice
logfile {_win_path(log_file)}

# ── Persistencia (RDB) ───────────────────────────────────────────────────────
# Guardado periódico. En desarrollo puedes comentar estas líneas.
save 900 1
save 300 10
save 60  10000
dbfilename dump.rdb
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes

# ── Memoria ──────────────────────────────────────────────────────────────────
# Ajustar según RAM disponible; 256 MB es suficiente para BookingScraper.
maxmemory 256mb
maxmemory-policy allkeys-lru

# ── Timeouts y keep-alive ────────────────────────────────────────────────────
timeout 0
tcp-keepalive 300

# ── Seguridad ────────────────────────────────────────────────────────────────
# Descomenta y cambia la contraseña en producción si expones el puerto.
# requirepass tu_password_aqui

# ── Rendimiento ──────────────────────────────────────────────────────────────
tcp-backlog 128
databases 16
hz 10
"""
    return conf


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera memurai.conf para BookingScraper Pro")
    parser.add_argument(
        "--base",
        type=str,
        default=None,
        help="Ruta base del proyecto (por defecto: directorio padre de este script)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Ruta de salida del archivo .conf (por defecto: <base>/memurai.conf)",
    )
    args = parser.parse_args()

    # Detectar base_dir
    if args.base:
        base_dir = Path(args.base).resolve()
    else:
        # El script vive en BASE_DIR/scripts/ → subir un nivel
        script_dir = Path(__file__).resolve().parent
        base_dir = script_dir.parent
        # Si el script se copia directamente a BASE_DIR, no subir
        if not (base_dir / "logs").exists() and (script_dir / "logs").exists():
            base_dir = script_dir

    if not base_dir.exists():
        print(f"[ERROR] Directorio base no existe: {base_dir}", file=sys.stderr)
        return 1

    output_path = Path(args.output).resolve() if args.output else base_dir / "memurai.conf"

    content = generate(base_dir)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] memurai.conf generado en:")
    print(f"     {output_path}")
    print(f"     base dir : {base_dir}")
    print(f"     logfile  : {base_dir / 'logs' / 'memurai.log'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
