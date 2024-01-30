"""schema

Revision ID: 59d641f915bf
Revises: 
Create Date: 2024-01-30 03:49:29.200852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59d641f915bf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_devices_id'), 'devices', ['id'], unique=False)
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('students',
        sa.Column('registration_no', sa.String(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('student_card_id', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('roll', sa.Integer(), nullable=True),
        sa.Column('batch', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('registration_no')
    )
    op.create_index(op.f('ix_students_registration_no'), 'students', ['registration_no'], unique=False)
    op.create_table('teachers',
        sa.Column('official_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('designation', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('official_id')
    )
    op.create_index(op.f('ix_teachers_official_id'), 'teachers', ['official_id'], unique=False)
    op.create_table('courses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('batch', sa.Integer(), nullable=True),
        sa.Column('teacher_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.official_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_classes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('course_id', sa.UUID(), nullable=True),
        sa.Column('class_time', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('course_class_id', sa.UUID(), nullable=True),
        sa.Column('student_id', sa.String(), nullable=True),
        sa.Column('is_present', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['course_class_id'], ['course_classes.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['students.registration_no'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_devices',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('course_class_id', sa.UUID(), nullable=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['course_class_id'], ['course_classes.id'], ),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course_devices')
    op.drop_table('attendance')
    op.drop_table('course_classes')
    op.drop_table('courses')
    op.drop_index(op.f('ix_teachers_official_id'), table_name='teachers')
    op.drop_table('teachers')
    op.drop_index(op.f('ix_students_registration_no'), table_name='students')
    op.drop_table('students')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_devices_id'), table_name='devices')
    op.drop_table('devices')
    # ### end Alembic commands ###
