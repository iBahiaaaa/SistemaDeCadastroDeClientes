from datetime import datetime
from typing import Optional, Dict, Any
from dateutil.relativedelta import relativedelta

PERIODO_MESES = {
    "mensal": 1,
    "trimestral": 3,
    "semestral": 6,
    "anual": 12
}


def calcular_meses_passados(data_inicio: str, data_fim: str) -> int:
    try:
        dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        dt_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

        meses = (
            (dt_fim.year - dt_inicio.year) * 12
            + (dt_fim.month - dt_inicio.month)
        )

        if dt_fim.day < dt_inicio.day:
            meses -= 1

        return max(0, meses)

    except Exception as e:
        print(f"[pagamento_service.py → erro no cálculo de meses passados: {e}")
        return 0


def calcular_proxima_data(data_base: str, plano: str) -> Optional[str]:
    try:
        dt_base = datetime.strptime(data_base, "%Y-%m-%d")

        meses = PERIODO_MESES.get(plano, 1)

        nova_data = dt_base + relativedelta(months=meses)

        return nova_data.strftime("%Y-%m-%d")

    except Exception as e:
        print(f"[pagamento_service.py → erro no cálculo da próxima data: {e}")
        return None


def verificar_status_pagamento_novo(
    cliente: Dict[str, Any],
    data_referencia: Optional[str] = None
) -> Dict[str, Any]:

    data_atual = datetime.now().date()

    data_ultimo_pagamento = cliente.get("ultimo_pagamento")
    data_vencimento_atual = cliente.get("data_vencimento")

    plano = cliente.get("plano", "mensal")
    meses_periodo = PERIODO_MESES.get(plano, 1)

    if not data_ultimo_pagamento or not data_vencimento_atual:
        return {
            "status_atual": "Pendente",
            "meses_vencidos": 0,
            "proxima_data_vencimento": datetime.now().strftime("%Y-%m-%d"),
            "data_ultimo_pagamento": data_ultimo_pagamento,
            "periodo_plano": plano
        }

    try:
        dt_vencimento = datetime.strptime(
            data_vencimento_atual,
            "%Y-%m-%d"
        ).date()

        data_ref = (
            datetime.strptime(data_referencia, "%Y-%m-%d").date()
            if data_referencia
            else data_atual
        )

        if data_ref < dt_vencimento:
            status = "Pago"
            meses_vencidos = 0

        else:
            meses_desde_vencimento = (
                (data_ref.year - dt_vencimento.year) * 12
                + (data_ref.month - dt_vencimento.month)
            )

            if data_ref.day >= dt_vencimento.day:
                meses_desde_vencimento += 1

            meses_vencidos = max(1, meses_desde_vencimento)

            if meses_vencidos >= 2:
                status = "Inadimplente"
            else:
                status = "Pendente"

        proxima_data = calcular_proxima_data(
            data_ultimo_pagamento,
            plano
        )

        return {
            "status_atual": status,
            "meses_vencidos": meses_vencidos,
            "proxima_data_vencimento": proxima_data,
            "data_ultimo_pagamento": data_ultimo_pagamento,
            "periodo_plano": plano
        }

    except Exception as e:
        print(f"[pagamento_service.py → erro na verificação do status: {e}")

        return {
            "status_atual": "Pendente",
            "meses_vencidos": 0,
            "proxima_data_vencimento": None,
            "data_ultimo_pagamento": data_ultimo_pagamento,
            "periodo_plano": plano
        }