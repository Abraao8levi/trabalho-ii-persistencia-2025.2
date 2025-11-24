#!/usr/bin/env python3
"""
Script para gerenciar migrações do banco de dados com suporte a SQLite e PostgreSQL
"""
import os
import subprocess
import sys

def load_dotenv_safe():
    """Tenta carregar dotenv e mostra configuração do banco"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv("DATABASE_URL", "sqlite:///./movie_app.db")
        db_type = "PostgreSQL" if "postgresql" in db_url else "SQLite"
        print(f"✅ {db_type} configurado via .env")
        print(f"🔗 Database URL: {db_url}")
        
    except ImportError:
        db_url = os.getenv("DATABASE_URL", "sqlite:///./movie_app.db")
        db_type = "PostgreSQL" if "postgresql" in db_url else "SQLite"
        print(f"⚠️  python-dotenv não instalado. Usando {db_type} do sistema.")
        print(f"🔗 Database URL: {db_url}")

def print_help():
    """Exibe ajuda dos comandos"""
    print("""
Uso: python migrate.py [comando] [opções]

Comandos disponíveis:
  init                    - Inicializa o alembic (primeira vez)
  create <message>        - Cria uma nova migração com mensagem
  upgrade [revision]      - Aplica migrações (head por padrão)
  downgrade [revision]    - Reverte migrações (-1 por padrão)
  history                 - Mostra histórico de migrações
  current                 - Mostra migração atual
  stamp <revision>        - Marca o banco como estando em uma revisão
  heads                   - Mostra heads de migração atuais
  check                   - Verifica se há migrações pendentes
  config                  - Mostra configuração atual do banco

Exemplos:
  python migrate.py init
  python migrate.py create "Adiciona tabela nova"
  python migrate.py upgrade
  python migrate.py config
    """)

def run_alembic_command(args):
    """Executa um comando alembic"""
    cmd = ["alembic"] + args
    
    # Mostra o comando sendo executado
    print(f"Executando: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Avisos:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {e}")
        if e.stdout:
            print("Saída:", e.stdout)
        if e.stderr:
            print("Erros:", e.stderr)
        return False
    except FileNotFoundError:
        print("❌ Erro: Alembic não encontrado. Instale com: pip install alembic")
        return False

def check_alembic_initialized():
    """Verifica se o alembic está inicializado"""
    return os.path.exists("alembic.ini") and os.path.exists("alembic")

def show_config():
    """Mostra configuração atual do banco"""
    db_url = os.getenv("DATABASE_URL", "sqlite:///./movie_app.db")
    db_type = "PostgreSQL" if "postgresql" in db_url else "SQLite"
    
    print("🔧 Configuração Atual do Banco de Dados:")
    print(f"   Tipo: {db_type}")
    print(f"   URL: {db_url}")
    print(f"   Arquivo .env: {'✅ Encontrado' if os.path.exists('.env') else '❌ Não encontrado'}")
    print(f"   Alembic: {'✅ Inicializado' if check_alembic_initialized() else '❌ Não inicializado'}")

def main():
    # Tenta carregar .env e mostra configuração
    load_dotenv_safe()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    # Comando especial para mostrar configuração
    if command == "config":
        show_config()
        return
    
    # Verifica se o alembic está inicializado para comandos que precisam
    if command not in ["init", "help", "--help", "-h"] and not check_alembic_initialized():
        print("❌ Alembic não inicializado. Execute primeiro:")
        print("   python migrate.py init")
        return
    
    if command == "init":
        if check_alembic_initialized():
            print("✅ Alembic já está inicializado")
            return
        
        print("🚀 Inicializando Alembic...")
        success = run_alembic_command(["init", "alembic"])
        if success:
            print("✅ Alembic inicializado com sucesso!")
            show_config()
        else:
            print("❌ Falha ao inicializar alembic")
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ Forneça uma mensagem para a migração")
            print("Uso: python migrate.py create \"Minha mensagem de migração\"")
            return
        
        message = sys.argv[2]
        print(f"📝 Criando migração: {message}")
        success = run_alembic_command(["revision", "--autogenerate", "-m", message])
        if success:
            print("✅ Migração criada com sucesso!")
        else:
            print("❌ Falha ao criar migração")
    
    elif command == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        print(f"⬆️  Aplicando migrações até: {revision}")
        success = run_alembic_command(["upgrade", revision])
        if success:
            print("✅ Migrações aplicadas com sucesso!")
        else:
            print("❌ Falha ao aplicar migrações")
    
    elif command == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
        print(f"⬇️  Revertendo migração para: {revision}")
        success = run_alembic_command(["downgrade", revision])
        if success:
            print("✅ Migração revertida com sucesso!")
        else:
            print("❌ Falha ao reverter migração")
    
    elif command == "history":
        print("📜 Histórico de migrações:")
        run_alembic_command(["history"])
    
    elif command == "current":
        print("📍 Migração atual:")
        run_alembic_command(["current"])
    
    elif command == "stamp":
        if len(sys.argv) < 3:
            print("❌ Forneça uma revisão para stamp")
            print("Uso: python migrate.py stamp <revision>")
            return
        
        revision = sys.argv[2]
        print(f"🏷️  Marcando banco como: {revision}")
        run_alembic_command(["stamp", revision])
    
    elif command == "heads":
        print("🗂️  Heads de migração:")
        run_alembic_command(["heads"])
    
    elif command == "check":
        print("🔍 Verificando migrações pendentes...")
        run_alembic_command(["check"])
    
    elif command in ["help", "--help", "-h"]:
        print_help()
    
    else:
        print(f"❌ Comando desconhecido: {command}")
        print_help()

if __name__ == "__main__":
    main()