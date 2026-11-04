--
-- PostgreSQL database dump
--

\restrict Fga4iYJbeSOdMympab42Xy2nTD5WAoBL9MGB3FJuX9DoD7kNFS8yqcrlbCkZ0I7

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.items (
    item_number character varying(30) NOT NULL,
    name character varying(30) NOT NULL,
    unit_measurement character varying(30) NOT NULL,
    cost integer NOT NULL,
    provider character varying(30) NOT NULL,
    manufacturer character varying(30) NOT NULL,
    item_category character varying(30) NOT NULL,
    current_discount integer NOT NULL,
    quantity_stock integer NOT NULL,
    description character varying(100) NOT NULL,
    photo character varying(30)
);


ALTER TABLE public.items OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_number integer NOT NULL,
    order_date date NOT NULL,
    delivery_date date NOT NULL,
    receipt_code integer NOT NULL,
    order_status character varying(30) NOT NULL,
    id_pickup_point integer,
    id_user integer
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_items (
    order_number integer NOT NULL,
    item_number character varying(30) NOT NULL,
    quantity integer
);


ALTER TABLE public.orders_items OWNER TO postgres;

--
-- Name: orders_order_number_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_order_number_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_order_number_seq OWNER TO postgres;

--
-- Name: orders_order_number_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_order_number_seq OWNED BY public.orders.order_number;


--
-- Name: pickup_points; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pickup_points (
    id integer NOT NULL,
    address character varying(100) NOT NULL
);


ALTER TABLE public.pickup_points OWNER TO postgres;

--
-- Name: pickup_points_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pickup_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pickup_points_id_seq OWNER TO postgres;

--
-- Name: pickup_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pickup_points_id_seq OWNED BY public.pickup_points.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    role character varying(30) NOT NULL,
    full_name character varying(30) NOT NULL,
    login character varying(30) NOT NULL,
    password character varying(30) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: orders order_number; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_number SET DEFAULT nextval('public.orders_order_number_seq'::regclass);


--
-- Name: pickup_points id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points ALTER COLUMN id SET DEFAULT nextval('public.pickup_points_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.items (item_number, name, unit_measurement, cost, provider, manufacturer, item_category, current_discount, quantity_stock, description, photo) FROM stdin;
S634B5	Кеды	шт.	5500	Обувь для вас	CROSBY	Мужская обувь	3	0	Кеды Caprice мужские демисезонные, размер 42, цвет черный	picture.png
J542F5	Тапочки	шт.	500	Kari	Kari	Мужская обувь	13	0	Тапочки мужские Арт.70701-55-67син р.41	picture.png
P764G4	Туфли	шт.	6800	Kari	CROSBY	Женская обувь	15	15	Туфли женские, ARGO, размер 38	picture.png
G783F5	Ботинки	шт.	5900	Kari	Рос	Мужская обувь	2	8	Мужские ботинки Рос-Обувь кожаные с натуральным мехом	G783F5.jpg
G531F4	Ботинки	шт.	6600	Kari	Kari	Женская обувь	12	8	Ботинки женские зимние ROMER арт. 893167-01 Черный	picture.png
O754F4	Туфли	шт.	5400	Обувь для вас	Rieker	Женская обувь	4	14	Туфли женские демисезонные Rieker артикул 55073-68/37	picture.png
E482R4	Полуботинки	шт.	1800	Kari	Kari	Женская обувь	2	14	Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный	picture.png
K345R4	Полуботинки	шт.	2100	Обувь для вас	CROSBY	Мужская обувь	2	3	407700/01-02 Полуботинки мужские CROSBY	picture.png
S213E3	Полуботинки	шт.	2156	Обувь для вас	CROSBY	Мужская обувь	3	6	407700/01-01 Полуботинки мужские CROSBY	picture.png
B431R5	Ботинки	шт.	2700	Обувь для вас	Rieker	Мужская обувь	2	5	Мужские кожаные ботинки/мужские ботинки	picture.png
А112Т4	Ботинки	шт.	4990	Kari	Kari	Женская обувь	3	6	Женские Ботинки демисезонные kari	1.jpg
F635R4	Ботинки	шт.	3244	Обувь для вас	Marco Tozzi	Женская обувь	2	13	Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый	2.jpg
H782T5	Туфли	шт.	4499	Kari	Kari	Мужская обувь	4	5	Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный	3.jpg
J384T6	Ботинки	шт.	3800	Обувь для вас	Rieker	Мужская обувь	2	16	B3430/14 Полуботинки мужские Rieker	5.jpg
D572U8	Кроссовки	шт.	4100	Обувь для вас	Рос	Мужская обувь	3	6	129615-4 Кроссовки мужские	6.jpg
F572H7	Туфли	шт.	2700	Kari	Marco Tozzi	Женская обувь	2	14	Туфли Marco Tozzi женские летние, размер 39, цвет черный	7.jpg
D329H3	Полуботинки	шт.	1890	Обувь для вас	Alessio Nesca	Женская обувь	4	4	Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый	8.jpg
B320R5	Туфли	шт.	4300	Kari	Rieker	Женская обувь	2	6	Туфли Rieker женские демисезонные, размер 41, цвет коричневый	9.jpg
G432E4	Туфли	шт.	2800	Kari	Kari	Женская обувь	3	15	Туфли kari женские TR-YR-413017, размер 37, цвет: черный	10.jpg
F427R5	Ботинки	шт.	11800	Обувь для вас	Rieker	Женская обувь	15	11	Ботинки на молнии с декоративной пряжкой FRAU	picture.png
N457T5	Полуботинки	шт.	4600	Kari	CROSBY	Женская обувь	3	13	Полуботинки Ботинки черные зимние, мех	picture.png
D364R4	Туфли	шт.	12400	Kari	Kari	Женская обувь	16	5	Туфли Luiza Belly женские Kate-lazo черные из натуральной замши	picture.png
S326R5	Тапочки	шт.	9900	Обувь для вас	CROSBY	Мужская обувь	17	15	Мужские кожаные тапочки "Профиль С.Дали" 	picture.png
L754R4	Полуботинки	шт.	1700	Kari	Kari	Женская обувь	2	7	Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный	picture.png
M542T5	Кроссовки	шт.	2800	Обувь для вас	Rieker	Мужская обувь	18	3	Кроссовки мужские TOFA	picture.png
D268G5	Туфли	шт.	4399	Обувь для вас	Rieker	Женская обувь	3	12	Туфли Rieker женские демисезонные, размер 36, цвет коричневый	picture.png
T324F5	Сапоги	шт.	4699	Kari	CROSBY	Женская обувь	2	5	Сапоги замша Цвет: синий	picture.png
K358H6	Тапочки	шт.	599	Kari	Rieker	Мужская обувь	20	2	Тапочки мужские син р.41	picture.png
H535R5	Ботинки	шт.	2300	Обувь для вас	Rieker	Женская обувь	2	7	Женские Ботинки демисезонные	picture.png
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (order_number, order_date, delivery_date, receipt_code, order_status, id_pickup_point, id_user) FROM stdin;
1	2025-02-27	2025-04-20	901	Завершен	1	4
2	2022-09-28	2025-04-21	902	Завершен	11	1
3	2025-03-21	2025-04-22	903	Завершен	2	2
4	2025-02-20	2025-04-23	904	Завершен	11	3
5	2025-03-17	2025-04-24	905	Завершен	2	4
6	2025-03-01	2025-04-25	906	Завершен	15	1
7	2025-02-28	2025-04-26	907	Завершен	3	2
8	2025-03-31	2025-04-27	908	Новый 	19	3
9	2025-04-02	2025-04-28	909	Новый 	5	4
10	2025-04-03	2025-04-29	910	Новый 	19	4
\.


--
-- Data for Name: orders_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_items (order_number, item_number, quantity) FROM stdin;
1	А112Т4	2
1	F635R4	2
2	H782T5	1
2	G783F5	1
3	J384T6	10
3	D572U8	10
4	F572H7	5
4	D329H3	4
5	А112Т4	2
5	F635R4	2
6	H782T5	1
6	G783F5	1
7	J384T6	10
7	D572U8	10
8	F572H7	5
8	D329H3	4
9	B320R5	5
9	G432E4	1
10	S213E3	5
10	E482R4	5
\.


--
-- Data for Name: pickup_points; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pickup_points (id, address) FROM stdin;
1	420151, г. Лесной, ул. Вишневая, 32
2	125061, г. Лесной, ул. Подгорная, 8
3	630370, г. Лесной, ул. Шоссейная, 24
4	400562, г. Лесной, ул. Зеленая, 32
5	614510, г. Лесной, ул. Маяковского, 47
6	410542, г. Лесной, ул. Светлая, 46
7	620839, г. Лесной, ул. Цветочная, 8
8	443890, г. Лесной, ул. Коммунистическая, 1
9	603379, г. Лесной, ул. Спортивная, 46
10	603721, г. Лесной, ул. Гоголя, 41
11	410172, г. Лесной, ул. Северная, 13
12	614611, г. Лесной, ул. Молодежная, 50
13	454311, г.Лесной, ул. Новая, 19
14	660007, г.Лесной, ул. Октябрьская, 19
15	603036, г. Лесной, ул. Садовая, 4
16	394060, г.Лесной, ул. Фрунзе, 43
17	410661, г. Лесной, ул. Школьная, 50
18	625590, г. Лесной, ул. Коммунистическая, 20
19	625683, г. Лесной, ул. 8 Марта
20	450983, г.Лесной, ул. Комсомольская, 26
21	394782, г. Лесной, ул. Чехова, 3
22	603002, г. Лесной, ул. Дзержинского, 28
23	450558, г. Лесной, ул. Набережная, 30
24	344288, г. Лесной, ул. Чехова, 1
25	614164, г.Лесной,  ул. Степная, 30
26	394242, г. Лесной, ул. Коммунистическая, 43
27	660540, г. Лесной, ул. Солнечная, 25
28	125837, г. Лесной, ул. Шоссейная, 40
29	125703, г. Лесной, ул. Партизанская, 49
30	625283, г. Лесной, ул. Победы, 46
31	614753, г. Лесной, ул. Полевая, 35
32	426030, г. Лесной, ул. Маяковского, 44
33	450375, г. Лесной ул. Клубная, 44
34	625560, г. Лесной, ул. Некрасова, 12
35	630201, г. Лесной, ул. Комсомольская, 17
36	190949, г. Лесной, ул. Мичурина, 26
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, role, full_name, login, password) FROM stdin;
1	Администратор	Никифорова Весения Николаевна	94d5ous@gmail.com	uzWC67
2	Администратор	Сазонов Руслан Германович	uth4iz@mail.com	2L6KZG
3	Администратор	Одинцов Серафим Артёмович	yzls62@outlook.com	JlFRCZ
4	Менеджер	Степанов Михаил Артёмович	1diph5e@tutanota.com	8ntwUp
5	Менеджер	Ворсин Петр Евгеньевич	tjde7c@yahoo.com	YOyhfR
6	Менеджер	Старикова Елена Павловна	wpmrc3do@tutanota.com	RSbvHv
7	Авторизированный клиент	Михайлюк Анна Вячеславовна	5d4zbu@tutanota.com	rwVDh9
8	Авторизированный клиент	Ситдикова Елена Анатольевна	ptec8ym@yahoo.com	LdNyos
9	Авторизированный клиент	Ворсин Петр Евгеньевич	1qz4kw@mail.com	gynQMT
10	Авторизированный клиент	Старикова Елена Павловна	4np6se@mail.com	AtnDjr
\.


--
-- Name: orders_order_number_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_order_number_seq', 2, true);


--
-- Name: pickup_points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pickup_points_id_seq', 36, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_number);


--
-- Name: orders_items orders_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_pkey PRIMARY KEY (order_number, item_number);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_number);


--
-- Name: pickup_points pickup_points_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pickup_points
    ADD CONSTRAINT pickup_points_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: orders orders_id_pickup_point_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_id_pickup_point_fkey FOREIGN KEY (id_pickup_point) REFERENCES public.pickup_points(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: orders orders_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: orders_items orders_items_item_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_item_number_fkey FOREIGN KEY (item_number) REFERENCES public.items(item_number) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: orders_items orders_items_order_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_order_number_fkey FOREIGN KEY (order_number) REFERENCES public.orders(order_number) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict Fga4iYJbeSOdMympab42Xy2nTD5WAoBL9MGB3FJuX9DoD7kNFS8yqcrlbCkZ0I7

