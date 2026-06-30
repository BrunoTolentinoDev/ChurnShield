"""Testes dos endpoints da API."""

from fastapi.testclient import TestClient


class TestAPI:
    def test_health(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app_name"] == "ChurnShield"

    def test_send_message_no_ai(self, client: TestClient) -> None:
        response = client.post(
            "/api/chat/message",
            json={"content": "Obrigado, estou satisfeito com o serviço!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["analysis"]["ia_called"] is False
        assert data["analysis"]["economy_registered"] is True

    def test_send_message_triggers_ai(self, client: TestClient) -> None:
        response = client.post(
            "/api/chat/message",
            json={
                "content": "Quero cancelar, está muito caro",
                "response_time_seconds": 90,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["analysis"]["ia_called"] is True
        assert len(data["analysis"]["rules_triggered"]) > 0
        assert data["analysis"]["risco_de_churn"] is not None

    def test_conversation_continuity(self, client: TestClient) -> None:
        r1 = client.post("/api/chat/message", json={"content": "Mensagem inicial longa aqui"})
        conv_id = r1.json()["conversation_id"]

        r2 = client.post(
            "/api/chat/message",
            json={"conversation_id": conv_id, "content": "Quero cancelar agora"},
        )
        assert r2.json()["conversation_id"] == conv_id
        assert r2.json()["analysis"]["ia_called"] is True

    def test_dashboard_metrics(self, client: TestClient) -> None:
        client.post("/api/chat/message", json={"content": "Tudo bem por aqui, obrigado!"})
        client.post("/api/chat/message", json={"content": "cancelar plano"})

        response = client.get("/api/dashboard/metrics")
        assert response.status_code == 200
        metrics = response.json()
        assert metrics["total_messages"] >= 2
        assert metrics["ai_calls"] >= 1
        assert metrics["ai_calls_avoided"] >= 1

    def test_decision_history(self, client: TestClient) -> None:
        client.post("/api/chat/message", json={"content": "reembolso urgente"})
        response = client.get("/api/dashboard/history/decisions")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_automation_history(self, client: TestClient) -> None:
        client.post(
            "/api/chat/message",
            json={"content": "cancelar tudo, insatisfeito"},
        )
        response = client.get("/api/dashboard/history/automations")
        assert response.status_code == 200
        logs = response.json()
        assert len(logs) >= 1
        assert any(l["action_type"] == "log_registered" for l in logs)
