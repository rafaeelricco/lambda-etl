--
-- PostgreSQL database dump
--

-- Dumped from database version 15.0 (Debian 15.0-1.pgdg110+1)
-- Dumped by pg_dump version 15.1

-- Started on 2022-12-09 14:16:22 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 214 (class 1259 OID 16610)
-- Name: cessao_fundo; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.cessao_fundo (
    id_cessao integer NOT NULL,
    originador character varying(250) NOT NULL,
    doc_originador numeric(50,0) NOT NULL,
    cedente character varying(250) NOT NULL,
    doc_cedente numeric(50,0) NOT NULL,
    ccb integer NOT NULL,
    id_externo integer NOT NULL,
    cliente character varying(250) NOT NULL,
    cpf_cnpj character varying(50) NOT NULL,
    endereco character varying(250) NOT NULL,
    cep character varying(50) NOT NULL,
    cidade character varying(250) NOT NULL,
    uf character varying(50) NOT NULL,
    valor_do_emprestimo numeric(10,2) NOT NULL,
    valor_parcela numeric(10,2) NOT NULL,
    total_parcelas integer NOT NULL,
    parcela integer NOT NULL,
    data_de_emissao date NOT NULL,
    data_de_vencimento date NOT NULL,
    preco_de_aquisicao numeric(10,2) NOT NULL
);


ALTER TABLE public.cessao_fundo OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16615)
-- Name: cessao_fundo_id_cessao_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.cessao_fundo_id_cessao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cessao_fundo_id_cessao_seq OWNER TO admin;

--
-- TOC entry 3328 (class 0 OID 0)
-- Dependencies: 215
-- Name: cessao_fundo_id_cessao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.cessao_fundo_id_cessao_seq OWNED BY public.cessao_fundo.id_cessao;


--
-- TOC entry 3176 (class 2604 OID 16616)
-- Name: cessao_fundo id_cessao; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.cessao_fundo ALTER COLUMN id_cessao SET DEFAULT nextval('public.cessao_fundo_id_cessao_seq'::regclass);


--
-- TOC entry 3321 (class 0 OID 16610)
-- Dependencies: 214
-- Data for Name: cessao_fundo; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.cessao_fundo (id_cessao, originador, doc_originador, cedente, doc_cedente, ccb, id_externo, cliente, cpf_cnpj, endereco, cep, cidade, uf, valor_do_emprestimo, valor_parcela, total_parcelas, parcela, data_de_emissao, data_de_vencimento, preco_de_aquisicao) FROM stdin;
\.


--
-- TOC entry 3329 (class 0 OID 0)
-- Dependencies: 215
-- Name: cessao_fundo_id_cessao_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.cessao_fundo_id_cessao_seq', 114, true);


--
-- TOC entry 3178 (class 2606 OID 16618)
-- Name: cessao_fundo cessao_fundo_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.cessao_fundo
    ADD CONSTRAINT cessao_fundo_pkey PRIMARY KEY (id_cessao);


-- Completed on 2022-12-09 14:16:22 UTC

--
-- PostgreSQL database dump complete
--

