from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserPreference(BaseModel):
    style: str
    club_type: str
    player_type: str


@app.get("/")
def home():
    return {"message": "EPL Recommendation API Running"}


@app.post("/recommend")
def recommend_team(user: UserPreference):
    scores = {
        "Arsenal": 0,
        "Manchester City": 0,
        "Manchester United": 0,
        "Liverpool": 0,
        "Chelsea": 0,
        "Tottenham Hotspur": 0
    }

    reasons = []

    if user.style == "공격적":
        scores["Liverpool"] += 3
        scores["Arsenal"] += 3
        scores["Manchester City"] += 2
        reasons.append("공격적인 축구를 선호함")
    elif user.style == "역습":
        scores["Tottenham Hotspur"] += 3
        scores["Manchester United"] += 2
        scores["Liverpool"] += 2
        reasons.append("빠른 역습과 전환 플레이를 선호함")
    elif user.style == "점유율":
        scores["Manchester City"] += 3
        scores["Arsenal"] += 2
        scores["Chelsea"] += 1
        reasons.append("점유율 중심의 경기를 선호함")
    else:
        scores["Chelsea"] += 3
        scores["Manchester United"] += 2
        scores["Tottenham Hotspur"] += 1
        reasons.append("균형 잡힌 경기 운영을 선호함")

    if user.club_type == "명문 구단":
        scores["Liverpool"] += 3
        scores["Manchester United"] += 3
        scores["Chelsea"] += 2
        reasons.append("전통과 인지도가 높은 팀을 선호함")
    elif user.club_type == "신흥 강호":
        scores["Arsenal"] += 3
        scores["Manchester City"] += 3
        scores["Chelsea"] += 1
        reasons.append("최근 성적과 성장세가 있는 팀을 선호함")
    else:
        scores["Tottenham Hotspur"] += 3
        scores["Chelsea"] += 1
        scores["Manchester United"] += 1
        reasons.append("낭만과 스토리가 있는 팀을 선호함")

    if user.player_type == "스트라이커":
        scores["Manchester City"] += 3
        scores["Tottenham Hotspur"] += 2
        scores["Liverpool"] += 1
        reasons.append("득점력이 강한 공격수를 좋아함")
    elif user.player_type == "윙어":
        scores["Liverpool"] += 3
        scores["Tottenham Hotspur"] += 3
        scores["Manchester United"] += 2
        reasons.append("빠르고 직선적인 윙어 플레이를 좋아함")
    else:
        scores["Arsenal"] += 3
        scores["Manchester City"] += 2
        scores["Chelsea"] += 2
        reasons.append("경기를 조율하는 플레이메이커를 좋아함")

    recommended_team = max(scores, key=scores.get)

    team_info = {
        "Arsenal": {
            "rank": "2025-26 시즌 최종 순위: 1위",
            "coach": "Mikel Arteta",
            "players": "Bukayo Saka, Martin Ødegaard, Declan Rice",
            "color": "Red / White",
            "difficulty": "쉬움",
            "description": "젊고 세련된 공격 축구와 안정적인 전력을 가진 팀입니다.",
            "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"
        },
        "Manchester City": {
            "rank": "2025-26 시즌 최종 순위: 2위",
            "coach": "Pep Guardiola",
            "players": "Erling Haaland, Phil Foden, Rodri",
            "color": "Sky Blue / White",
            "difficulty": "쉬움",
            "description": "점유율 축구와 조직적인 패스 플레이가 강한 현대적인 강팀입니다.",
            "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"
        },
        "Manchester United": {
            "rank": "2025-26 시즌 최종 순위: 3위",
            "coach": "Michael Carrick",
            "players": "Bruno Fernandes, Kobbie Mainoo, Alejandro Garnacho",
            "color": "Red / Black",
            "difficulty": "보통",
            "description": "전통과 팬덤이 강한 명문 구단으로, 스토리가 많은 팀입니다.",
            "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"
        },
        "Liverpool": {
            "rank": "2025-26 시즌 최종 순위: 5위",
            "coach": "Arne Slot",
            "players": "Mohamed Salah, Virgil van Dijk, Dominik Szoboszlai",
            "color": "Red",
            "difficulty": "쉬움",
            "description": "강한 압박, 빠른 공격 전개, 뜨거운 팬 문화가 특징인 팀입니다.",
            "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"
        },
        "Chelsea": {
            "rank": "2025-26 시즌 최종 순위: 10위",
            "coach": "Liam Rosenior",
            "players": "Cole Palmer, Enzo Fernández, Reece James",
            "color": "Blue / White",
            "difficulty": "보통",
            "description": "젊은 선수층과 화려한 런던 클럽 이미지가 강한 팀입니다.",
            "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg"
        },
        "Tottenham Hotspur": {
            "rank": "2025-26 시즌 최종 순위: 17위",
            "coach": "Igor Tudor",
            "players": "Son Heung-min, James Maddison, Cristian Romero",
            "color": "White / Navy",
            "difficulty": "어려움",
            "description": "빠른 역습, 윙어 중심 공격, 낭만적인 응원 문화가 특징인 팀입니다.",
            "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"
        }
    }

    info = team_info[recommended_team]

    return {
        "team": recommended_team,
        "score": scores[recommended_team],
        "selected_reasons": reasons,
        "all_scores": scores,
        "rank": info["rank"],
        "coach": info["coach"],
        "players": info["players"],
        "color": info["color"],
        "difficulty": info["difficulty"],
        "description": info["description"],
        "logo_url": info["logo_url"]
    }