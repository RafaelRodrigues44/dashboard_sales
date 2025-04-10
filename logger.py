import logging

# Configuração básica do logger
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
