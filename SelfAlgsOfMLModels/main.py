import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report as report,
    mean_squared_error as mse,
    r2_score as r2
)
from sklearn.tree import (
    DecisionTreeClassifier as Dtc,
    DecisionTreeRegressor as Dtr
)
from cart import CART

st.set_page_config(
    page_title="Model CART",
    page_icon="🌲"
)

session = st.session_state

st.header('🌲Model CART🌲', divider='rainbow')
st.subheader('Classification And Regression Tree')

# Загрузка датасета #
st.subheader(':blue[1. Загрузите датасет]')
st.file_uploader(
    label='Uploader',
    key='file',
    label_visibility='collapsed'
)

if session['file'] and 'df' not in session:
    session['df'] = pd.read_csv(session['file'])
elif not session['file']:
    session.clear()

# Выбор признаков #
if 'df' in session:
    st.subheader(':blue[2. Выберите целевую переменную]')
    target = st.selectbox(
        label='Target',
        options=[None] + session.df.columns.tolist(),
        key='target',
        label_visibility='collapsed'
    )

# разделение на тренировочную и тестовую выборку #
if 'target' in session and session['target']:
    session['x'] = session['df'].drop(
        session['target'], axis=1)
    session['y'] = session['df'][session['target']]

# Настройки модели #
if 'x' in session:
    st.subheader(':blue[3. Настройте модель]')

    criterion = st.selectbox(
        label='Метрика:',
        options= [
         'squared_error',
         'absolute_error',
         'entropy',
         'gini'
        ])

    session['is_regression'] = criterion in [
         'squared_error','absolute_error']

    st.text_input(
        label='Глубина:',
        key='max_depth',
        placeholder='По умолчанию: не ограничено')
    try:
        max_depth = int(session['max_depth'])
    except ValueError as e:
        max_depth = None

    st.text_input(
        label='Минимальный размер листа для сплита',
        key='min_samples_split',
        placeholder='По умолчанию: 2')
    try:
        min_samples_split = int(
            session['min_samples_split'])
    except Exception as e:
        min_samples_split = 2

    session['cart'] = CART(
        criterion=criterion,
        max_depth=max_depth,
        min_samples_split=min_samples_split)

    if session['is_regression']:
        session['sklearn_model'] = Dtr(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split
            )
    else:
        session['sklearn_model'] = Dtc(
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split
            )

    st.button(
        label='Далее',
        key='model_settings',
        use_container_width=True)

def metrics(y_test, predict):
    if session['is_regression']:
        st.subheader(f'MSE: {mse(y_test, predict).round(3): _}')
        st.subheader(f'R^2: {r2 (y_test, predict).round(3)}')
    else:
        st.write(pd.DataFrame(report(y_test, predict, output_dict=True)))

# обучение модели и результаты #
if 'model_settings' in session and session['model_settings']:
    st.subheader(':blue[4. Результаты]')
    x_tr, x_test, y_tr, y_test = train_test_split(
        session['x'],
        session['y'],
        test_size=0.2,
        random_state=42)

    with st.spinner('Модель обучается...'):
        session['cart'].fit(x_tr, y_tr)

    predict = session['cart'].predict(x_test)
    metrics(y_test, predict)

    st.subheader(':blue[5. Сравнение с sklearn]')

    session['sklearn_model'].fit(x_tr, y_tr)
    predict = session['sklearn_model'].predict(x_test)
    metrics(y_test, predict)
