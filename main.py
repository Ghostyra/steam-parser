def Main():
    from steam_parser import SteamParser
    steam_hentai = SteamParser()
    steam_hentai.set_url("https://store.steampowered.com/search/?tags=24904&category1=998")
    steam_hentai.parsing()
    #print(steam_hentai.parse_data("https://store.steampowered.com/app/981800/Hentai_University_2_Biology_course/?snr=1_7_7_240_150_9"))

if __name__ == "__main__":
    Main()
