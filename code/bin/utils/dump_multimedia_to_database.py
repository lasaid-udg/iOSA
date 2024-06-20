import sys
import os
import re
import json
# Laptop
sys.path.append(r"C:\Users\zaira\GitHub\inSAsy")
# PC
# sys.path.append(r"C:\Users\EricG\GitHub\inSAsy")

from database import MultimediaDb, ControllDb


def dump_multimedia_backup_to_database() -> None:
    # laptop
    front_photo_path = r"C:\Users\zaira\GitHub\inSAsy\multimedia\photos\front"
    lateral_photo_path = r"C:\Users\zaira\GitHub\inSAsy\multimedia\photos\lateral"
    # video_path = r"C:\Users\zaira\GitHub\inSAsy\multimedia\videos"
    # audio_path = r"C:\Users\zaira\GitHub\inSAsy\multimedia\audios"
    # osa_path = r"C:\Users\zaira\GitHub\inSAsy\multimedia\osa"
    # PC
    # front_photo_path = r"C:\Users\EricG\GitHub\inSAsy\multimedia\photos\front"
    # lateral_photo_path = r"C:\Users\EricG\GitHub\inSAsy\multimedia\photos\lateral"
    # video_path = r"C:\Users\EricG\GitHub\inSAsy\multimedia\videos"
    # audio_path = r"C:\Users\EricG\GitHub\inSAsy\multimedia\audios"
    # osa_path = r"C:\Users\EricG\GitHub\inSAsy\multimedia\osa"

    delete_all_documents_of_all_collection()
    add_front_photos_to_database(front_photo_path)
    add_lateral_photos_to_database(lateral_photo_path)
    # add_videos_to_database(video_path)
    # add_audios_to_database(audio_path)
    # add_osas_to_database(osa_path)
    print("Dump succesful...")


def delete_all_documents_of_all_collection() -> None:
    db_multimedia = MultimediaDb()
    db_multimedia.delete_front_photo()
    db_multimedia.delete_lateral_photo()
    db_multimedia.delete_video()
    db_multimedia.delete_audio()
    db_multimedia.delete_osa()


def add_front_photos_to_database(front_photo_path) -> None:
    extension = ".jpg"
    file_list = list()

    for x in os.listdir(front_photo_path):
        if x.endswith(extension):
            file_list.append(x)
    
    if len(file_list) == 0:
        print("No files found...")
    else:
        for file in file_list:
            db_multimedia = MultimediaDb()
            db_control = ControllDb()
            relative_front_photo_path = r"multimedia\photos\front"
            backup_photo_data = db_control.selectTagPicture(
                re.search(r"\d+",file).group(),
                0
            )
            if backup_photo_data is not None:
                front_photo_data = (
                    backup_photo_data[1],
                    relative_front_photo_path + '\\' + file,
                    json.dumps(backup_photo_data[2]),
                    0
                )
                db_multimedia.insert_front_photo(front_photo_data)


def add_lateral_photos_to_database(lateral_photo_path) -> None:
    extension = ".jpg"
    file_list = list()

    for x in os.listdir(lateral_photo_path):
        if x.endswith(extension):
            file_list.append(x)
    
    if len(file_list) == 0:
        print("No files found...")
    else:
        for file in file_list:
            db_multimedia = MultimediaDb()
            db_control = ControllDb()
            relative_lateral_photo_path = r"multimedia\photos\lateral"
            backup_photo_data = db_control.selectTagPicture(
                re.search(r"\d+",file).group(),
                1
            )
            if backup_photo_data is not None:
                lateral_photo_data = (
                    backup_photo_data[1],
                    relative_lateral_photo_path + '\\' + file,
                    json.dumps(backup_photo_data[2]),
                    1
                )
                db_multimedia.insert_lateral_photo(lateral_photo_data)


def add_videos_to_database(video_path) -> None:
    extension = ".mp4"
    file_list = list()

    for x in os.listdir(video_path):
        if x.endswith(extension):
            #print(x)
            file_list.append(x)
    
    if len(file_list) == 0:
        print("No files found...")
    else:
        for file in file_list:
            db_multimedia = MultimediaDb()
            relative_video_path = r"multimedia\videos"
            front_photo_data = (
                re.search(r"\d+",file).group(),
                relative_video_path
            )
            db_multimedia.insert_video(front_photo_data)


def add_audios_to_database(audio_path) -> None:
    extension = ".mp3"
    file_list = list()

    if len(file_list) == 0:
        print("No files found...")
    else:
        for file in file_list:
            db_multimedia = MultimediaDb()
            relative_audio_path = r"multimedia\audios"
            audio_data = (
                re.search(r"\d+",file).group(),
                relative_audio_path
            )
            db_multimedia.insert_audio(audio_data)


def add_osas_to_database(osa_path) -> None:
    extension = ".osa"
    file_list = list()

    for x in os.listdir(osa_path):
        if x.endswith(extension):
            #print(x)
            file_list.append(x)
    
    if len(file_list) == 0:
        print("No files found...")
    else:
        for file in file_list:
            db_multimedia = MultimediaDb()
            relative_osa_path = r"multimedia\audios"
            osa_data = (
                re.search(r"\d+",file).group(),
                relative_osa_path
            )
            db_multimedia.insert_osa(osa_data)


if __name__ == '__main__':
    dump_multimedia_backup_to_database()