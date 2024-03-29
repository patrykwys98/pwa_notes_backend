from fastapi import HTTPException, status
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.share import Share
from app.schemas.note import (NotesAndSharedNotesSchema, NoteSchema,
                              NotesToTreeSchema, SharedNoteSchema)
from app.schemas.user import UserSchema
from app.utils.note import (not_owner_and_not_can_delete,
                            not_owner_and_not_can_edit)


async def add_note(
    db: Session,
    note: NoteSchema,
    user: UserSchema
) -> Note:
    db_note = Note(
        title=note.title,
        content=note.content,
        child_id=note.child_id,
        owner_id=user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


async def get_note(
    db: Session,
    note_id: int,
    user: UserSchema
) -> Note:
    is_shared_for_user = db.query(Share).filter(
        Share.note_id == note_id, Share.user_id == user.id).first()
    is_owner = db.query(Note).filter(
        Note.id == note_id, Note.owner_id == user.id).first()
    if not is_shared_for_user and not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't access this note"
        )
    note = db.query(Note).filter(
        and_(Note.id == note_id, user.id == user.id)).first()
    return note


async def delete_note(
    db: Session,
    note_id: int,
    user: UserSchema
) -> Note:
    if not_owner_and_not_can_delete(db, user.id, note_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete this note"
        )
    note = db.query(Note).filter(
        and_(Note.id == note_id, user.id == user.id)).first()
    shared = db.query(Share).filter(Share.note_id == note_id).all()
    if shared:
        for share in shared:
            db.delete(share)
    note.shared = []
    childrens = db.query(Note).filter(Note.child_id == note_id).all()
    if childrens:
        for child in childrens:
            child.child_id = None
    db.delete(note)
    db.commit()
    return note


async def update_note(
    db: Session,
    note_id: int,
    note: NoteSchema,
    user: UserSchema
) -> Note:
    if not_owner_and_not_can_edit(db, user.id, note_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't edit this note"
        )
    db_note = db.query(Note).filter(
        and_(Note.id == note_id, user.id == user.id)).first()
    db_note.title = note.title
    db_note.content = note.content
    db_note.child_id = note.child_id
    db.commit()
    db.refresh(db_note)
    return db_note


async def rename_note(
    db: Session,
    note_id: int,
    title: str,
    user: UserSchema
) -> Note:
    if not_owner_and_not_can_edit(db, user.id, note_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't edit this note"
        )
    db_note = db.query(Note).filter(
        and_(Note.id == note_id, Note.owner_id == user.id)).first()
    db_note.title = title
    db.commit()
    db.refresh(db_note)
    return db_note


async def get_notes_and_shared_notes(
    db: Session,
    user: UserSchema
) -> NotesAndSharedNotesSchema:
    notes = db.query(Note).filter(Note.owner_id == user.id).all()
    shared_notes = db.query(Note).filter(Note.shared.any(user_id=user.id)).all()
    notes = list(map(lambda x: NotesToTreeSchema.from_orm(x), notes))
    shared_notes = list(map(lambda x: SharedNoteSchema.from_orm(x), shared_notes))
    return NotesAndSharedNotesSchema(notes=notes, shared=shared_notes)


async def update_tree_structure(
    db: Session,
    q: list[NotesToTreeSchema],
    user: UserSchema
) -> NotesToTreeSchema:
    for note in q:
        db_note = db.query(Note).filter(
            and_(Note.id == note.id, Note.owner_id == user.id)).first()
        db_note.child_id = note.child_id
        db.commit()
        db.refresh(db_note)
    return note


async def search_in_title_and_content(
    db: Session,
    query: str,
    user: UserSchema
) -> list[NotesToTreeSchema]:
    notes = db.query(Note).filter(
        or_(Note.title.like(f"%{query}%"), Note.content.like(f"%{query}%"))).all()
    notes = list(map(lambda x: NotesToTreeSchema.from_orm(x), notes))
    return notes
