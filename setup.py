import os
import sys
import platform
import time
# import tweetminer
import nltk


def setup():
    intro = "Downloading nltk packages for"
    osys = str(platform.system())

    if osys == "Windows":
        print(intro + " " + osys + "...\n")
        time.sleep(2)

        # find full path to the current venv
        win_venv = os.getenv('VIRTUAL_ENV')

        # point to NLTK_DATA in the venv
        win_data = win_venv + '\\lib\\nltk_data'
        os.environ['NLTK_DATA'] = win_data

        try:
            os.mkdir(win_venv + '\\lib\\nltk_data')
        except FileExistsError:
            print("nltk_data already exists!")
            # needs error explanation
            pass

        try:
            nltk.download('punkt', download_dir=win_venv + '\\lib\\nltk_data')
            nltk.download('words', download_dir=win_venv + '\\lib\\nltk_data')
            nltk.download('stopwords', download_dir=win_venv + '\\lib\\nltk_data')
        except Exception as e:
            print("nltk_error: %s" % str(e))

    elif osys == "Linux":
        print(intro + " " + osys + "...\n")
        time.sleep(2)

        # find full path to the current venv
        lin_venv = os.getenv('VIRTUAL_ENV')

        # get the current python version
        pyver = "python" + str(sys.version_info[0])+"."+str(sys.version_info[1])

        # point to NLTK_DATA in the venv
        lin_data = lin_venv + '/lib/' + pyver + '/nltk_data'
        os.environ['NLTK_DATA'] = lin_data

        try:
            os.mkdir(lin_data)
        except FileExistsError:
            print("nltk_data already exists!")
            pass

        try:
            nltk.download('punkt', download_dir=lin_data)
            nltk.download('words', download_dir=lin_data)
            nltk.download('stopwords', download_dir=lin_data)
        except Exception as e:
            print("nltk_error: %s" % str(e))

    else:
        print(intro + osys + "...\n")
        print("Wait...nevermind, get outta here with your busted " + osys + " OS")
        print("Goodbye...")
        time.sleep(3)
        sys.exit()

    print("DONE!\nNow launching main menu...")
    time.sleep(2)
    return


if __name__ == '__main__':
    setup()
    # tweetminer.menu()
