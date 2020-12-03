def Main():
    from steam_parser import SteamParser
    steam_hentai = SteamParser()
    steam_hentai.set_url("https://store.steampowered.com/search/?tags=9130&category1=998")
    steam_hentai.parsing()
    #print(steam_hentai.parse_data("https://store.steampowered.com/app/893180/Catherine_Classic/"))

if __name__ == "__main__":
    Main()
