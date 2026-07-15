import asyncio
from app.db.session import AsyncSessionLocal
from app.db.models.usuarios import Usuario, PlanoEnum
from app.db.models.vagas import Vaga, FonteVagaEnum
from app.db.models.trajetorias import Trajetoria, FonteDadoEnum

async def seed():
    async with AsyncSessionLocal() as session:
        # Check if users exist
        # Just a simple seed for testing local data
        user = Usuario(
            nome="João Teste",
            email="joao.teste@example.com",
            senha_hash="hash_falso",
            cidade="São Paulo",
            estado="SP",
            plano=PlanoEnum.free
        )
        session.add(user)
        
        vaga = Vaga(
            titulo_cargo="Engenheiro de Software",
            empresa="Tech Corp",
            cidade="São Paulo",
            estado="SP",
            fonte=FonteVagaEnum.linkedin,
            url_original="http://linkedin.com/vaga/123",
            hash_deduplicacao="hash123",
            ativa=True
        )
        session.add(vaga)
        
        trajetoria = Trajetoria(
            cargo_origem="Desenvolvedor Junior",
            cargo_destino="Desenvolvedor Pleno",
            tempo_medio_meses=24,
            fonte_dado=FonteDadoEnum.real
        )
        session.add(trajetoria)

        await session.commit()
        print("Database seeded with sample data.")

if __name__ == "__main__":
    asyncio.run(seed())
