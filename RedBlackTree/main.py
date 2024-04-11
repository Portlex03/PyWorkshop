from redblacktree import RedBlackTree
import matplotlib.pyplot as plt
import streamlit as st
import networkx as nx
import random
import time

st.set_page_config(
    page_title="RedBlackTree",
    page_icon="🌲"
)

session = st.session_state

if 'tree' not in session:
    session.tree = RedBlackTree()

if 'inserted_values' not in session:
    session.inserted_values = []

if 'session_iteration' not in session:
    session.session_iteration = 0

st.title('🌲:red[Красно] - :gray[чёрное] :green[дерево]🌲')

sidebar = st.sidebar
sidebar.title('⚙️Настройки дерева')

# вставка чисел
sidebar.subheader('🔢Вставка')
sidebar.text_input(label='Введите числа:', key='insert_field', placeholder='Пример: 56 17 8 46', label_visibility='collapsed')
def clear_insert_text():
    session.new_values = session.insert_field
    session["insert_field"] = ""
sidebar.button(label='Вставить', key='insert_button', on_click=clear_insert_text, use_container_width=True)

# поиск элемента
sidebar.subheader('Поиск')
value = sidebar.text_input(label='Введите число:', key='search_field', placeholder='Пример: 34', label_visibility='collapsed')
if sidebar.button(label='Найти', key='search_button', use_container_width=True) and value:
    node = session.tree.search(int(value))
    if node:
        st.success(f'Найден узел {value}', icon='✅')
    else:
        st.warning(f'Не найдено: {value}', icon='⚠️')

# удаление чисел
sidebar.subheader('🗑 Удаление чисел')
sidebar.text_input(
    label='Введите числа:',
    placeholder='Пример: 16 5 4 23 1',
    key='values2delete',
    label_visibility='collapsed'
)
def clear_delete_text():
    session.deleting_values = session.values2delete
    session["values2delete"] = ""
sidebar.button(label='Удалить', key='delete_button', on_click=clear_delete_text, use_container_width=True)

# вставка случайных числел
sidebar.subheader('🎲Вставка случайных чисел')
random_insert_holder = st.sidebar.empty()
random_insert_slider = random_insert_holder.slider(
    label='🔽Определите их количество:',
    key=f'insert_slider_{session.session_iteration}',
    max_value=10
)
def insert_random():
    session.session_iteration += 1
    random_insert_values_count = session[f"insert_slider_{session.session_iteration - 1}"]
    sequence = set(range(1, 1000)) - set(session.inserted_values)
    values = random.sample(list(sequence), random_insert_values_count)
    session.tree.insert_from(values)
    session.inserted_values.extend(values)
    if values:
        st.success(f'Успешно добавлены значения {values}', icon='✅')
sidebar.button(label='Вставить', key='random_insert_button', on_click=insert_random, use_container_width=True)


# Удаление случайных чисел
sidebar.subheader('🎲Удаление случайных чисел')
random_deleting_holder = st.sidebar.empty()
random_deleting_slider = random_deleting_holder.slider(
    label='🔽Определите их количество:',
    key=f'delete_slider_{session.session_iteration}',
    max_value=10
)
def delete_random():
    session.session_iteration += 1
    random_deleting_values_count = session[f"delete_slider_{session.session_iteration - 1}"]
    if random_deleting_values_count >= len(session.inserted_values):
        session.tree = RedBlackTree()
        session.inserted_values = []
        session.session_iteration = 0
        st.success(f'Успешно удалено дерево', icon='✅')
    else:
        values = random.sample(session.inserted_values, random_deleting_values_count)
        session.tree.delete_from(values)
        for value in values:
            session.inserted_values.remove(value)
        if values:
            st.success(f'Успешно удалены значения: {values}', icon='✅')
sidebar.button(label='Удалить', key='random_delete_button', on_click=delete_random, use_container_width=True)

sidebar.header('👀 Настройки отображения')
figsize = sidebar.slider(
    label='📸Размер изображения',
    min_value=3,
    max_value=20
)
margins = sidebar.slider(
    label='↖️Размер рёбер',
    min_value=0.0,
    max_value=0.7,
    step=0.02,
    value=0.4
)

font_size = sidebar.slider(
    label='✏️Размер шрифта узлов',
    min_value=8,
    max_value=32,
    value=12
)
node_size = sidebar.slider(
    label='🌀Размер узлов',
    min_value=500,
    max_value=5000,
    step=100
)

def visualization():
    tree = session.tree
    g, pos, options = tree.realize(font_size, node_size)
    fig = plt.figure(figsize=[figsize]*2)
    plt.title('Визуализация')
    plt.axis('off')
    nx.draw_networkx(g, pos, **options)
    plt.margins(margins)
    st.pyplot(fig)

if session.insert_button:
    try:
        new_values = set([
            int(value) for value in 
                session.new_values.split()
        ])
    except ValueError as e:
        new_values = None
        st.error(f'⛔️Неправильный ввод: {e}')

    correct_values = []
    wrong_values = []
    for value in new_values:
        try:
            session.tree.insert(value)
            session.inserted_values.append(value)
            correct_values.append(value)
        except ValueError:
            wrong_values.append(value)
    if correct_values:
        st.success(f'Успешно добавлено: {correct_values}', icon='✅')
    if wrong_values:
        st.warning(f'Не добавлено: {wrong_values}', icon='⚠️')

if session.delete_button:
    try:
        values2delete = set([
            int(value) for value in 
                session.deleting_values.split()
        ])
    except ValueError as e:
        values2delete = None
        st.error(f'⛔️Неправильный ввод: {e}')

    correct_values = []
    wrong_values = []
    for value in values2delete:
        try:
            session.tree.delete(value)
            session.inserted_values.remove(value)
            correct_values.append(value)
        except ValueError:
            wrong_values.append(value)
    if correct_values:
        st.success(f'Успешно удалено: {correct_values}', icon='✅')
    if wrong_values:
        st.warning(f'Не удалено: {wrong_values}', icon='⚠️')

if session.inserted_values:
    with st.spinner('Загрузка...'):
        time.sleep(2)
    st.subheader(f'👽Вставленные значения: {sorted(session.inserted_values)}')
    visualization()
