# ▼ 기존 코드에서 이 부분만 수정하면 돼요 ▼

# ==========================================
# 선택 국가 데이터
# ==========================================
country_data = df[df["Country"] == selected_country].iloc[0]

# MBTI 데이터만 추출
values = country_data[mbti_types]

# ------------------------------------------
# 🔥 높은 비율 순으로 정렬 추가
# ------------------------------------------
sorted_values = values.sort_values(ascending=False)

sorted_mbti = sorted_values.index
sorted_scores = sorted_values.values

# 가장 높은 값 index
max_index = 0

# ------------------------------------------
# 색상 설정
# ------------------------------------------
colors = []

green_shades = [
    "#d8f3dc",
    "#b7e4c7",
    "#95d5b2",
    "#74c69d",
    "#52b788",
    "#40916c",
    "#2d6a4f",
    "#1b4332"
]

green_idx = 0

for i in range(len(sorted_scores)):
    if i == max_index:
        colors.append("#ff1493")  # 핫핑크
    else:
        colors.append(
            green_shades[
                green_idx % len(green_shades)
            ]
        )
        green_idx += 1

# ------------------------------------------
# 그래프 생성
# ------------------------------------------
fig1, ax1 = plt.subplots(figsize=(12, 6))

bars = ax1.bar(
    sorted_mbti,
    sorted_scores,
    color=colors
)

ax1.set_title(
    f"{selected_country}의 MBTI 비율",
    fontsize=18,
    fontweight="bold"
)

ax1.set_xlabel("MBTI 유형")
ax1.set_ylabel("비율")

plt.xticks(rotation=45)

# 값 표시
for bar in bars:
    height = bar.get_height()

    ax1.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:.2%}",
        ha='center',
        va='bottom',
        fontsize=9
    )

st.pyplot(fig1)

# ------------------------------------------
# 최고 MBTI 표시
# ------------------------------------------
top_mbti = sorted_mbti[0]
top_value = sorted_scores[0]

st.success(
    f"💖 {selected_country}에서 가장 높은 MBTI는 "
    f"**{top_mbti}** ({top_value:.2%}) 입니다!"
)
