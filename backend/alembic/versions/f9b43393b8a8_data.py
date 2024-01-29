"""data

Revision ID: f9b43393b8a8
Revises: 32b65c428357
Create Date: 2024-01-30 02:27:21.017928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9b43393b8a8'
down_revision: Union[str, None] = '32b65c428357'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # generate user
    op.bulk_insert(
        sa.table('users',
            sa.column('id', sa.UUID()),
            sa.column('name', sa.String()),
            sa.column('email', sa.String()),
            sa.column('password', sa.String()),
            sa.column('role', sa.String()),         
        ),
        [
            {
                "id": "f0f8a8e4-7b1e-4c4f-9e6a-4e2c5f0c2f3e",
                "name": "Tushar",
                "email": "tushar@du.ac.bd",
                "password": "maple-leaf-1234",
                "role": "teacher",

            }
        ]
    )


    # generate teacher
    op.bulk_insert(
        sa.table('teachers',
            sa.column('official_id', sa.Integer()),
            sa.column('user_id', sa.UUID()),
            sa.column('designation', sa.String()),         
        ),
        [
            {
                "official_id": 1234,
                "user_id": "f0f8a8e4-7b1e-4c4f-9e6a-4e2c5f0c2f3e",
                "designation": "Professor",
            }
        ]
    )

    # generate course
    op.bulk_insert(
        sa.table('courses',
            sa.column('id', sa.UUID()),
            sa.column('code', sa.String()),
            sa.column('name', sa.String()),
            sa.column('year', sa.Integer()),
            sa.column('batch', sa.Integer()),
            sa.column('teacher_id', sa.Integer()),
        ),
        [
            {
                "id": "f0f8a8e4-7b1e-4c4f-9e6a-4e2c5f0c2f3e",
                "code": "CSE-3103",
                "name": "Microprocessor and Mircocontroller",
                "year": 2023,
                "batch": 27,
                "teacher_id": 1234,
            }
        ]
    )

    # generate device
    op.bulk_insert(
        sa.table('devices',
            sa.column('id', sa.Integer()),
            sa.column('name', sa.String()),
            sa.column('is_active', sa.Boolean()),         
        ),
        [
            {
                "id": 1,
                "name": "Pilot",
                "is_active": True,
            }
        ]
    )

    # generate course_device
    op.bulk_insert(
        sa.table('course_devices',
            sa.column('id', sa.UUID()),
            sa.column('course_id', sa.UUID()),
            sa.column('device_id', sa.Integer()),         
        ),
        [
            {
                "id": "f0f8a8e4-7b1e-4c4f-9e6a-4e2c5f0c2f3e",
                "course_id": "f0f8a8e4-7b1e-4c4f-9e6a-4e2c5f0c2f3e",
                "device_id": 1,
            }
        ]
    )


def downgrade() -> None:
    pass
