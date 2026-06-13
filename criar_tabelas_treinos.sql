-- Criação da tabela de exercícios
CREATE TABLE IF NOT EXISTS exercicios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    grupo_muscular VARCHAR(100) NOT NULL,
    nivel_experiencia VARCHAR(50) NOT NULL, -- iniciante/intermediario/avancado
    restricoes_lesao TEXT -- Lista de lesões que NÃO podem fazer esse exercício, separadas por vírgula
);

-- Criação da tabela de treinos
CREATE TABLE IF NOT EXISTS treinos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    nivel_experiencia VARCHAR(50) NOT NULL,
    tem_lesao BOOLEAN NOT NULL DEFAULT FALSE,
    local_lesao VARCHAR(100),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Criação da tabela de relação entre treinos e exercícios
CREATE TABLE IF NOT EXISTS treino_exercicios (
    id SERIAL PRIMARY KEY,
    treino_id INT NOT NULL,
    exercicio_id INT NOT NULL,
    series INT NOT NULL,
    repeticoes VARCHAR(50) NOT NULL,
    ordem INT NOT NULL,
    FOREIGN KEY (treino_id) REFERENCES treinos(id) ON DELETE CASCADE,
    FOREIGN KEY (exercicio_id) REFERENCES exercicios(id) ON DELETE CASCADE
);

-- Inserir exercícios padrão
INSERT INTO exercicios (nome, grupo_muscular, nivel_experiencia, restricoes_lesao) VALUES
-- Iniciante
('Supino Reto com Barra', 'Peito', 'iniciante', 'ombro,punho'),
('Rosca Direta com Barra', 'Bíceps', 'iniciante', 'punho,cotovelo'),
('Agachamento com Peso Corporal', 'Pernas', 'iniciante', 'joelho,coluna'),
('Cadeira Extensora', 'Pernas (Quadríceps)', 'iniciante', 'joelho'),
('Puxada Alta no Pulley', 'Costas', 'iniciante', 'ombro,coluna'),
('Tríceps no Banco', 'Tríceps', 'iniciante', 'ombro,punho'),
('Leg Press', 'Pernas', 'iniciante', 'joelho,coluna'),
('Elevamento Lateral com Halteres', 'Ombros', 'iniciante', 'ombro'),
-- Intermediário
('Supino Inclinado com Halteres', 'Peito', 'intermediario', 'ombro,punho'),
('Rosca Martelo', 'Bíceps', 'intermediario', 'punho'),
('Agachamento com Barra', 'Pernas', 'intermediario', 'joelho,coluna'),
('Cadeira Flexora', 'Pernas (Isquiotibiais)', 'intermediario', 'joelho'),
('Remada Curvada com Barra', 'Costas', 'intermediario', 'coluna,lombar'),
('Tríceps Testa', 'Tríceps', 'intermediario', 'ombro,punho,cotovelo'),
('Stiff', 'Pernas', 'intermediario', 'coluna,lombar'),
('Desenvolvimento com Halteres', 'Ombros', 'intermediario', 'ombro'),
-- Avançado
('Supino Declinado com Barra', 'Peito', 'avancado', 'ombro,punho'),
('Rosca Concentrada', 'Bíceps', 'avancado', 'punho,cotovelo'),
('Agachamento Frontal', 'Pernas', 'avancado', 'joelho,coluna'),
('Cadeira Abdutora', 'Pernas (Glúteos)', 'avancado', 'joelho'),
('Remada Unilateral com Halter', 'Costas', 'avancado', 'coluna,lombar,ommbro'),
('Tríceps no Pulley com Corda', 'Tríceps', 'avancado', 'ombro,punho'),
('Sumo Deadlift', 'Pernas', 'avancado', 'coluna,lombar,joelho'),
('Desenvolvimento Arnold', 'Ombros', 'avancado', 'ombro');
