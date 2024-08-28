FROM python

WORKDIR /app

COPY API_SERVER.py          \ 
    api_requests.py         \
    clean_cache.sh          \
    image_classifier.py     \
    ImageNet_classes.json   \
    main.py                 \
    MY_modules.py           \
    mysql_DB.py             \
    requirements.txt        \
    DB_DUMP.sql             \
    /app/

RUN mkdir /app/Models
RUN mkdir /app/Models/vit-base-patch16-224/
COPY Models/vit-base-patch16-224/ /app/Models/vit-base-patch16-224/

RUN apt-get update
RUN apt-get install -y default-mysql-client
# RUN mysql -ugroot -piamgroot -P 3306 -h db < DB_Dump.sql

RUN pip install -r /app/requirements.txt

EXPOSE 5002

CMD python API_SERVER.py