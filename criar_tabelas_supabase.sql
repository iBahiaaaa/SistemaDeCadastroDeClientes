-- Criação da tabela clientes
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT,
    whatsapp TEXT,
    endereco TEXT,
    plano TEXT,
    valor_plano NUMERIC,
    periodo_plano TEXT DEFAULT 'mensal',
    data_matricula TEXT,
    data_vencimento TEXT,
    ultimo_pagamento TEXT,
    contato_emergencia TEXT,
    status TEXT,
    observacoes TEXT
);

-- Criação da tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT,
    cargo TEXT NOT NULL CHECK (
        cargo IN ('ADM', 'FUNCIONARIO', 'INSTRUTOR', 'FINANCEIRO', 'ALUNO')
    ),
    cliente_id INTEGER UNIQUE REFERENCES clientes(id) ON DELETE SET NULL,
    activation_code TEXT,
    activation_created_at TEXT
);

-- Habilita a extensão para UUID (opcional)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
