import mysql.connector
import json
import glob
from MY_modules import vidName_from_path

'''
mysqldump -u groot -p search_engine videos categories video_categories > "D:\\Code Space\\Projects\\Video Transcription\\SETUP\\DB_Backup.sql"
'''

db = mysql.connector.connect(
    host="localhost", # "db" for docker | # "localhost" for non docker execution
    user="groot",
    password="iamgroot",
    database = "search_engine"
)


def insert_imagenet_categories(json_file):
    dbcursor = db.cursor()
    with open(json_file, 'r') as f:
        data = json.load(f)

    try:
        for class_id, category_name in data.items():
            sql = f'INSERT INTO categories VALUES ("{class_id}","{category_name}")'
            dbcursor.execute(sql)
        db.commit()

        print("------------INSERT INTO categories: Successful------------")

    except mysql.connector.Error as error:
        if error.errno == 1062:
            pass
        else:
            print("Error inserting ImageNet categories into categories table:", error)

    finally:
        dbcursor.close()


def insert_videos(vid_dir:str="Shorts_Videos"):
    dbcursor = db.cursor()

    try:
        vid_files = vidName_from_path(vid_dir_path=vid_dir)
        vid_paths = glob.glob(vid_dir+'/*')
        vid_paths = [path.replace('\\', '/') for path in vid_paths]
        for i,file_name in enumerate(vid_files):
            query = f"SELECT file_name from videos where file_name='{file_name}'"
            dbcursor.execute(query)
            result=dbcursor.fetchone()

            if result:
                print(f"Video File: {result} already exists in DB")
                continue

            query = f'INSERT INTO videos (file_name,file_path) VALUES ("{file_name}","{vid_paths[i]}")'
            dbcursor.execute(query)

        db.commit()
        print("------------INSERT INTO videos: Successful------------")

    except mysql.connector.Error as error:
        print("Error inserting video data into videos table:", error)

    finally:
        dbcursor.close()


def category_To_category_id(category_name:str):
    try:
        dbcursor = db.cursor()
        query = f"SELECT category_id from categories where category_name = '{category_name}'"
        dbcursor.execute(query)
        category_id = dbcursor.fetchone()

    except mysql.connector.Error as error:
        print("Error extracting category_id from categories table:", error)
    finally:
        dbcursor.close()
        return category_id[0]


def video_To_video_id(video_name:str):
    try:
        dbcursor = db.cursor()
        query = f"SELECT video_id from videos WHERE file_name='{video_name}'"
        dbcursor.execute(query)
        video_id = dbcursor.fetchone()
        
    except mysql.connector.Error as error:
        print("Error extracting video_id from videos table:", error)
    finally:
        dbcursor.close()
        return video_id[0]


def check_indexed_state(video_name:str):
    dbcursor = db.cursor()
    try:
        query = f"SELECT index_state from videos WHERE file_name='{video_name}'"
        dbcursor.execute(query)
        index_state = dbcursor.fetchone()

    except mysql.connector.Error as error:
        print("Error retriving index_state:", error)

    finally:
        dbcursor.close()
        return index_state[0]


def sort_video_categories_table():
    dbcursor = db.cursor()
    
    try:
        count_frequency = '''UPDATE video_categories AS vc
                INNER JOIN (
                SELECT video_id, category_id, COUNT(*) AS frequency
                FROM video_categories
                GROUP BY video_id, category_id
                ) AS freq_table
                ON vc.video_id = freq_table.video_id AND vc.category_id = freq_table.category_id
                SET vc.frequency = freq_table.frequency;'''
        sort_table = '''ALTER TABLE video_categories
                    ORDER BY video_id, frequency DESC;'''
        create_view = '''CREATE VIEW video_index AS
                SELECT videos.video_id, videos.file_name, videos.file_path, categories.category_id ,categories.category_name, COUNT(*) AS frequency
                FROM videos
                LEFT JOIN video_categories ON videos.video_id = video_categories.video_id
                LEFT JOIN categories ON video_categories.category_id = categories.category_id
                GROUP BY videos.video_id, videos.file_name, categories.category_name, categories.category_id;'''
        
        
        dbcursor.execute(count_frequency)
        dbcursor.execute(sort_table)
        db.commit()

        print(f"$$ Table (video_categories) updated with category_frequency and sorted")

        dbcursor.execute(create_view)
        db.commit()

    except mysql.connector.Error as error:
        if error.errno == 1050:
            pass
        else:
            print("Error counting frequency and sorting videos table:", error)

    finally:
        dbcursor.close()


def insert_video_categories(json_file):
    dbcursor = db.cursor()
    
    try:
        with open(json_file, "r") as file:
            indexed_data = json.load(file)
     
        for i in range(0,len(indexed_data["keyframes_classified"])):
            video_id = video_To_video_id(indexed_data["src_file"])
            category_name = f"{indexed_data["keyframes_classified"][f'{i}']["category"]}".strip("[]").replace("'","")
            category_id = category_To_category_id(category_name)
            query = f"INSERT INTO video_categories (video_id, category_id) VALUES ('{video_id}','{category_id}');"
            dbcursor.execute(query)

            query = f"UPDATE videos SET index_state = 1 WHERE video_id = {video_id};"
            dbcursor.execute(query)
            print(f"$$ New video {indexed_data["src_file"]} indexed")
        sort_video_categories_table()
        db.commit()

    except mysql.connector.Error as error:
        print("Error inserting data into MySQL table:", error)

    finally:
        dbcursor.close()


def search_video(search_tag:str):
    try:
        dbcursor = db.cursor()
        query = f"select file_path,file_name,category_name from search_engine.video_index where category_name like '%{search_tag}%';"
        dbcursor.execute(query)
        result=dbcursor.fetchall()
        if result:
            path = result[0][0]
            file_name = result[0][1]
            category_list = result[0][2]
            search_result = {"file_path":path,
                             "file_name":file_name,
                             "category_list":category_list}
            # print("Video Search Results:")
            # print("File_name: ",file_name)
            # print("Path: ",path)
            # print("Category: ",category_list)
            return search_result
        else:
            print("$$ No match Found")

    except mysql.connector.Error as error:
        print("Error Searching video from Video_Index:", error)


# insert_imagenet_categories("ImageNet_classes.json")
# insert_videos("Shorts_Videos")
# insert_video_categories("market")
# search_video("pencil")
# sort_video_categories_table()