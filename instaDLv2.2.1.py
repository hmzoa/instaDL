#!/usr/bin/env python
import argparse
import datetime
import random
import string
import os
import sys
try:
    import colorama 
    import requests
except:
    try:
        os.system("pip install -r requirements.txt")
    except:
        try:
            os.system("pip install colorama")
            os.system("pip install requests")
        except:exit()
        print("requirements.txt not found .")
colorama.init()
colorama.Fore.RESET
sended = colorama.Fore.LIGHTWHITE_EX + " [" + colorama.Fore.LIGHTGREEN_EX + "*" + colorama.Fore.LIGHTWHITE_EX + "] "
annowns = colorama.Fore.LIGHTWHITE_EX + " [" + colorama.Fore.LIGHTRED_EX + "!" + colorama.Fore.LIGHTWHITE_EX + "] "
msgFromProg = colorama.Fore.LIGHTWHITE_EX + " [" + colorama.Fore.LIGHTYELLOW_EX + "~" + colorama.Fore.LIGHTWHITE_EX + "] "
added = colorama.Fore.LIGHTWHITE_EX + " [" + colorama.Fore.GREEN + "+" + colorama.Fore.LIGHTWHITE_EX + "] "
error_ = colorama.Fore.LIGHTWHITE_EX + " [" + colorama.Fore.RED + "ERROR" + colorama.Fore.LIGHTWHITE_EX + "] "
logo = f"""{colorama.Fore.MAGENTA}  
  _           _        ____  _     
 (_)_ __  ___| |_ __ _|  _ \| |    
 | | '_ \/ __| __/ _` | | | | |    
 | | | | \__ \ || (_| | |_| | |___ 
 |_|_| |_|___/\__\__,_|____/|_____|
                        {colorama.Fore.LIGHTBLACK_EX}by - @hmzoa{colorama.Fore.RESET}
"""
class instaDL:
    def __init__(self) -> None:
        self.versionUrl : str = "https://raw.githubusercontent.com/hmzoa/instaDL/main/Version"
        self.currentVersion : str = "2.2.1"
        self.currentFile : str = __file__.split("\\")[-1]
        parser = argparse.ArgumentParser(
                description=f'{added}a script to download any media from instagram',
                usage=f"{colorama.Fore.LIGHTBLACK_EX}python {colorama.Fore.LIGHTWHITE_EX}{self.currentFile} {colorama.Fore.RESET}[-h] [-l {colorama.Fore.LIGHTCYAN_EX}<media-link>{colorama.Fore.RESET}] [-s {colorama.Fore.LIGHTGREEN_EX}<session-id>{colorama.Fore.RESET}] [-d] [{colorama.Fore.LIGHTCYAN_EX}<media-link>{colorama.Fore.RESET}]",
                epilog=f"{colorama.Fore.LIGHTRED_EX}───────────────────────────────────────┘{colorama.Fore.YELLOW}⌠{colorama.Fore.LIGHTBLACK_EX}by @hmzoa{colorama.Fore.YELLOW}⌡{colorama.Fore.LIGHTRED_EX}┌───────────────────────────────────────"
            )
        parser.add_argument('link',nargs='?',metavar='<media-link>',type=str,help=f'{colorama.Fore.GREEN}the post url link{colorama.Fore.RESET}',default="empty")
        parser.add_argument('-l','--link',dest='link_flag',type=str,metavar='<media-link>',help='the post url link',default="empty")
        parser.add_argument('-s','--sessionid',type=str,metavar='<session-id>',help='sessionid of an account that follows the private profile ',default="empty")
        debugMode = parser.add_mutually_exclusive_group()
        debugMode.add_argument('-d','--debug',action='store_true',help="turn on debug mode to print requests responses")
        self.args = parser.parse_args()
        self.url : str = self.args.link if self.args.link != "empty" else self.args.link_flag        
        self.sessionid : str = self.args.sessionid 
        self.pk : str = ""
        self.mediaName : str = ""
        self.mediaNameList : list = []
        print(logo)
        if len(sys.argv)==1:
            parser.print_help()
        elif self.sessionid == "empty" :
            self.publicMediaDL()
        elif self.sessionid != "empty" :
            self.privateMediaDL()
        else:
            ""#working on it : login with user and password to download private post python instaDL.py https://intsgram.com/examplePost -u username -p    
        self.lastFunc()
    def lastFunc(self):
        try:
            getVersion = requests.get(self.versionUrl).text.replace("\n","")
            if getVersion != self.currentVersion:
                print(f"\n{colorama.Fore.LIGHTRED_EX}  -  you are running older version v{self.currentVersion}")
                print(f"{colorama.Fore.LIGHTGREEN_EX}  -  version v{getVersion} is available on https://github.com/hmzoa/instaDL/")
            exit()
        except:exit()
    def publicMediaDL(self):
        print(f"{msgFromProg}Conforming URL.")
        if self.conformUrl():
            print(f"{sended}Conformed successfully.")
            print(f"{msgFromProg}Downloading media now.")
            if self.downloadInstaMedia():
                if self.mediaName.split('-')[1] == "GraphSidecar": print(f"{added}multiple media successfully Downloaded from user : ( {colorama.Fore.CYAN + self.mediaName.split('-')[0] + colorama.Fore.RESET})")
                else:print(f"{added}The media successfully Downloaded as : ({colorama.Fore.CYAN + self.mediaName + colorama.Fore.RESET})")
            else :
                print(f"{error_}Somthing went wrong , the media did not download successfully.")
        else:
            print(f"{annowns}Invalid URL {colorama.Fore.LIGHTYELLOW_EX + str(self.url) } .")
            
    def privateMediaDL(self):
            print(f"{msgFromProg}Conforming URL.")
            if self.conformUrl():
                print(f"{sended}Conformed successfully.")
                print(f"{msgFromProg}Downloading media now.")
                if self.downloadInstaMedia():
                    print(f"{added}The media successfully Downloaded as : ({colorama.Fore.CYAN + self.mediaName + colorama.Fore.RESET})")
                else :
                    print(f"{error_}Somthing went wrong , the media did not download successfully.")
            else:
                print(f"{annowns}Invalid URL {colorama.Fore.LIGHTYELLOW_EX + str(self.url) } .")
                
    def conformUrl(self):
        if self.url != "empty":
            if self.url.startswith("https://www.instagram.com/"):#"https://www.instagram.com/" in self.url:
                if "?" in self.url:
                    self.url=self.url.split("?")[0] + "?__a=1&__d=dis"
                    if self.args.debug:print(self.url)
                else:
                    if self.url[-1] != "/":
                        self.url = self.url + "/"
                        if self.args.debug:print(self.url)
                    self.url = self.url + "?__a=1&__d=dis"
                    if self.args.debug:print(self.url)
                return True
            else:
                return False
        else:
            return False
    def downloadInstaMedia(self):
        if self.sessionid == "empty":
            getDLurl = requests.request(
                "GET",
                url=self.url,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                    'cookie':'ig_did=7E1A5C43-633C-4514-9181-070791BD757D; ds_user_id=25025320',#22187948569
                    "X-CSRFtoken": "ZhhR4RZU5U9qxG8cOXZ8kj1Oq8fB5aH9"
                },
            )
            if self.args.debug:print(getDLurl.text)
            try :
                if getDLurl.text == '{"message":"Please wait a few minutes before you try again.","require_login":true,"status":"fail"}':return False 
                else:jsonLoaded = getDLurl.json() 
            except : return False
            if jsonLoaded["graphql"]["shortcode_media"]["__typename"] == "GraphVideo":#"GraphImage"
                try:
                    DLurl = jsonLoaded["graphql"]["shortcode_media"]["video_url"]
                except KeyError:return False
                downloadReq = requests.get(DLurl ,stream=True )
                if self.args.debug:print(downloadReq)
                self.mediaName = f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} _ {str(datetime.datetime.now()).split(".")[0].replace(":","-")}.mp4'
                try :os.mkdir("instaVideos")
                except FileExistsError : pass
                with open(f'instaVideos/{self.mediaName}','wb') as f:
                    f.write(downloadReq.content)
                    f.flush()
                return True
            elif jsonLoaded["graphql"]["shortcode_media"]["__typename"] == "GraphImage":
                try:
                    DLurl = jsonLoaded["graphql"]["shortcode_media"]["display_url"]
                    if self.args.debug:print(DLurl)
                except KeyError:return False
                downloadReq = requests.get(DLurl ,stream=True )
                if self.args.debug:print(downloadReq)
                self.mediaName = f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} _ {str(datetime.datetime.now()).split(".")[0].replace(":","-")}.jpg'
                try : os.mkdir("instaPhotos")
                except FileExistsError : pass
                with open(f'instaPhotos/{self.mediaName}','wb') as f:
                    f.write(downloadReq.content)
                    f.flush()
                return True
            elif jsonLoaded["graphql"]["shortcode_media"]["__typename"] == "GraphSidecar":
                for item in jsonLoaded["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]:
                    try :
                        if item["node"]["__typename"] == "GraphImage":
                            self.mediaName = f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} - {str(datetime.datetime.now()).split(".")[0].replace(":","-")} - {str(item["node"]["display_resources"][-1]["src"]).split("?")[0].split("/")[-1]}'#f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} _ {str(datetime.datetime.now()).split(".")[0].replace(":","-")}.jpg'
                            DLurl = item["node"]["display_resources"][-1]["src"]
                            if self.args.debug:print(DLurl)
                            downloadReq = requests.get(DLurl ,stream=True )
                            if self.args.debug:print(downloadReq)
                            try : os.mkdir("instaPhotos")
                            except FileExistsError : pass
                            with open(f'instaPhotos/{self.mediaName}','wb') as f:
                                f.write(downloadReq.content)
                                f.flush()
                        elif item["node"]["__typename"] == "GraphVideo":
                            self.mediaName = f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} - {str(datetime.datetime.now()).split(".")[0].replace(":","-")} - {str(item["node"]["video_url"]).split("?")[0].split("/")[-1]}'#self.mediaName = f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} _ {str(datetime.datetime.now()).split(".")[0].replace(":","-")}.mp4'
                            DLurl = item["node"]["video_url"]
                            if self.args.debug:print(DLurl)
                            downloadReq = requests.get(DLurl ,stream=True )
                            if self.args.debug:print(downloadReq)
                            try : os.mkdir("instaVideos")
                            except FileExistsError : pass
                            with open(f'instaVideos/{self.mediaName}','wb') as f:
                                f.write(downloadReq.content)
                                f.flush()
                        print(f'  -  {colorama.Fore.LIGHTBLACK_EX}Media done {colorama.Fore.LIGHTGREEN_EX}√{colorama.Fore.RESET}')
                    except:return False 
                self.mediaName = f'{jsonLoaded["graphql"]["shortcode_media"]["owner"]["username"]} -GraphSidecar'
                return True
                
            else : return False
        elif self.sessionid != "empty":
            try:self.pk = self.sessionid.split('%')[0]
            except:return False
            getDLurl_S = requests.request(
                "GET",
                url=self.url,
                headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',},
                cookies={
                    "sessionid":f"{self.sessionid}",
                    "ds_user_id":f"{self.pk}",
                    "csrftoken":"".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32))
                }
            )
            if self.args.debug:print(getDLurl_S.text)
            
            try :
                if getDLurl_S.text == '{"message":"Please wait a few minutes before you try again.","require_login":true,"status":"fail"}':return False 
                else:jsonLoaded_S = getDLurl_S.json() 
            except : return False
            if 'video_versions' in getDLurl_S.text and "image_versions2" in getDLurl_S.text:#its video post
                try :
                    DLurl_S = jsonLoaded_S["items"][0]["video_versions"][0]["url"]
                    if self.args.debug:print(DLurl_S)
                except KeyError:return False
                downloadReq = requests.get(DLurl_S ,stream=True )
                if self.args.debug:print(downloadReq)
                self.mediaName = f'{jsonLoaded_S["items"][0]["user"]["username"]} _ {str(datetime.datetime.now()).split(".")[0].replace(":","-")}.mp4'
                try :os.mkdir("instaVideos")
                except FileExistsError : pass
                with open(f'instaVideos/{self.mediaName}','wb') as f:
                    f.write(downloadReq.content)
                    f.flush()
                return True
            elif "image_versions2" in getDLurl_S.text and "video_versions" not in getDLurl_S.text:#its image post
                try :
                    DLurl_S = jsonLoaded_S["items"][0]["image_versions2"]["candidates"][0]["url"]
                    if self.args.debug:print(DLurl_S)
                except KeyError:return False
                downloadReq = requests.get(DLurl_S ,stream=True )
                if self.args.debug:print(downloadReq)
                self.mediaName = f'{jsonLoaded_S["items"][0]["user"]["username"]} _ {str(datetime.datetime.now()).split(".")[0].replace(":","-")}.jpg'
                try :os.mkdir("instaPhotos")
                except FileExistsError : pass
                with open(f'instaPhotos/{self.mediaName}','wb') as f:
                    f.write(downloadReq.content)
                    f.flush()
                return True
            else:
                if self.args.debug:print("non of options")
                return False
if __name__ == '__main__':
    app = instaDL()