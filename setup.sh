# Script para iniciar o container do banco de dados MySQL
docker run --name=backend_labtel_container \
  --restart on-failure \
  -e MYSQL_ROOT_PASSWORD=seguranca101 \
  -e MYSQL_DATABASE=backend_labtel_db \
  -p 3306:3306 \
  -d mysql/mysql-server

echo "Aguardando container iniciar..."

# Aguardar o container iniciar
while ! docker exec backend_labtel_container mysqladmin ping -h localhost --silent; do
  sleep 1
done

sleep 5

echo "Container iniciado com sucesso!"

# Configurar permissões no MySQL para permitir conexões remotas
docker exec -i backend_labtel_container mysql -uroot -pseguranca101 -e "
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'seguranca101';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
"

echo "Permissões configuradas para conexões remotas!"

# Script para criar o ambiente virtual e executar as migrações do banco de dados
python3 -m venv .venv

source .venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Dependências instaladas com sucesso!"

# Criar migração inicial do banco de dados
alembic revision --autogenerate -m "initial" --rev-id 1

# Executar as migrações do Alembic
alembic upgrade head

echo "Tabelas criadas com sucesso pelo Alembic!"

# # Executar o script para popular o banco de dados
docker exec -i backend_labtel_container mysql -uroot -pseguranca101 backend_labtel_db < ./db/init.sql
echo "Banco de dados inicializado com sucesso!"

echo "Migrações do banco de dados aplicadas com sucesso!"