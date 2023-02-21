from functions import send_hi, Manga, check_on_wikipedia, cat_fact, tendencia, anime, moedas, dado, agradeciment, traducao


def processing(answer, message):

    message = message

    match answer:

        case "pesquisa":
            return check_on_wikipedia(message)
        
        case "gatos":
            return cat_fact()

        case "tendencias":
            return tendencia()

        case "anime":
            return anime()

        case "dado":
            return dado(message)

        case "manga/webtoon":
            return Manga(message)
        
        case "ola":
            return send_hi()
        
        case "agradecimento":
            return agradeciment()
        
        case "tradução":
            return traducao(message)