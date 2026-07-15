import pytest
from sqlalchemy.exc import IntegrityError
from app.db.models.usuarios import Usuario, PlanoEnum
from app.db.models.curriculos import Curriculo
from app.db.models.clusters import Cluster

@pytest.mark.asyncio
async def test_usuario_unique_email(db_session):
    u1 = Usuario(nome="Test 1", email="test@example.com", senha_hash="hash1", plano=PlanoEnum.free)
    db_session.add(u1)
    await db_session.commit()
    
    u2 = Usuario(nome="Test 2", email="test@example.com", senha_hash="hash2", plano=PlanoEnum.free)
    db_session.add(u2)
    
    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

@pytest.mark.asyncio
async def test_cascade_delete_curriculo(db_session):
    u1 = Usuario(nome="Test 3", email="test3@example.com", senha_hash="hash3", plano=PlanoEnum.free)
    db_session.add(u1)
    await db_session.commit()
    await db_session.refresh(u1)
    
    c1 = Curriculo(usuario_id=u1.id, arquivo_url="http://s3.com/123.pdf")
    db_session.add(c1)
    await db_session.commit()
    
    # Delete user, should delete curriculo
    await db_session.delete(u1)
    await db_session.commit()
    
    # Check if curriculo still exists
    result = await db_session.get(Curriculo, c1.id)
    assert result is None

@pytest.mark.asyncio
async def test_cluster_no_fk_usuario(db_session):
    # Verify via reflection or simply asserting columns
    # We can inspect the Cluster model to ensure it has no foreign keys referencing 'usuarios'
    fk_columns = [col for col in Cluster.__table__.columns if col.foreign_keys]
    assert len(fk_columns) == 0, "Clusters should not have any foreign keys to reconstruct identities."
