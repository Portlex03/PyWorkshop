from redblacktree import RedBlackTree
import streamlit as st

st.set_page_config(
    page_title="RedBlackTree",
    page_icon="🌲"
)

if 'values_list' not in st.session_state:
    st.session_state.values_list = set()

if 'tree' not in st.session_state:
    st.session_state.tree = RedBlackTree()

if 'image' not in st.session_state:
    st.session_state.image = None

st.title('🌲:red[Красно] - :gray[чёрное] :green[дерево]🌲')

st.subheader('🔢 Введите числа, которые хотите вставить:')

st.text_input(
    'Введите числа:',
    label_visibility='collapsed',
    placeholder='Пр: 1 2 3 4 5',
    key='new_values'
)

sidebar = st.sidebar
sidebar.title('Настройки дерева')

font_size = sidebar.selectbox(
    label='Размер шрифта узлов',
    options=range(12, 19)
)

node_size = sidebar.slider(
    label='Размер узлов',
    min_value=500,
    max_value=3500,
    step=100,
    value=1000
)

figsize = sidebar.selectbox(
    label='Размер изображения',
    options=range(5, 13)
)

margins = sidebar.slider(
    label='Размер рёбер',
    min_value=0.05,
    max_value=0.7,
    step=0.05,
    value=0.4
)

try:
    new_values = set([
        int(value) for value in 
            st.session_state.new_values.split()
    ])
except ValueError as e:
    new_values = None
    st.error(f'⛔️Неправильный ввод: {e}')

if st.button('🎯Добавить'):
    if not new_values:
        st.error('⛔️Вы должны ввести значение, чтоб оно добавилось')
    elif len(new_values - st.session_state.values_list) == 0:
        st.warning('⚠️Уникальных значений нет. В дерево ничего не добавилось')
    else:
        new_values -= st.session_state.values_list

        st.session_state.tree.add_nodes_from(list(new_values))

        st.session_state.values_list = \
            st.session_state.values_list.union(new_values)

if st.session_state.values_list:

    output = [
        node.value for node in 
            st.session_state.tree._nodes if node.value]

    st.subheader(f'✅Узлы дерева: {output}')

    st.subheader('📈Визуализация:')

    if st.button('Нарисовать или перезагрузить дерево') or st.session_state.image:
        st.session_state.image = st.session_state.tree.image(
            font_size=font_size,
            node_size=node_size,
            figsize=(figsize, figsize),
            margins=margins
        )
        st.pyplot(st.session_state.image)

        if st.button('Очистить дерево'):
            st.session_state.clear()
            st.rerun()
