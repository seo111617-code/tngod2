# ① 전처리: 음수·비정상적으로 큰 값을 결측치로 바꾸기
MAX_VALUE = {'SO2': 1.0, 'NO2': 2.0, 'O3': 0.5, 'CO': 50.0, 'PM10': 600.0, 'PM25': 500.0}
for col in pollutants:
    wrong = (df[col] < 0) | (df[col] > MAX_VALUE[col])
    df.loc[wrong, col] = np.nan

# ② 하루 평균으로 바꾸고 '어제'·'내일' 열 만들기
daily = df.groupby('date')[pollutants].mean()
daily = daily.asfreq('D')
daily['PM25_yesterday'] = daily['PM25'].shift(1)
daily['target'] = daily['PM25'].shift(-1)

# ③ 시간 순서로 학습/평가 나누고 모델 비교
train = daily[daily.index.year < 2019]
test = daily[daily.index.year == 2019]
lr = LinearRegression().fit(X_train, y_train)
best_name = min(candidates, key=lambda n: mean_absolute_error(y_test, candidates[n].predict(X_test)))

# ④ 등급 판정
def pm25_grade(value):
    if value <= 15: return '좋음'
    elif value <= 35: return '보통'
    elif value <= 75: return '나쁨'
    return '매우나쁨'
