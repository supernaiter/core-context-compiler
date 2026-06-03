from __future__ import annotations

from corectx.rendering.dsl_renderer import DslRenderer
from corectx.schemas import MemoryAtom, MemoryLoadout


def build_prompt_block(loadout: MemoryLoadout, atoms_by_id: dict[str, MemoryAtom]) -> str:
    renderer = DslRenderer()
    ordered_ids = [*loadout.global_core, *loadout.project_core, *loadout.task_pack]
    atoms = [atoms_by_id[atom_id] for atom_id in ordered_ids if atom_id in atoms_by_id]
    return renderer.render_core_block(atoms)
