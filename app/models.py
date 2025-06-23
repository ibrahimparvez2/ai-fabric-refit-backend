from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class BlendMaterial(BaseModel):
    material: str
    percentage: float

class HexValue(BaseModel):
    name: str
    hex: str

class MaterialComposition(BaseModel):
    primary_material: str
    blend_materials: List[BlendMaterial] = []
    notes: Optional[str] = None


class ColorPalette(BaseModel):
    primary_color: str
    secondary_colors: List[str] = []
    accent_colors: List[str] = []
    hex_values: List[HexValue] = []


class PatternCharacteristics(BaseModel):
    pattern_type: Optional[str] = None
    pattern_repeat_size: Optional[str] = None
    pattern_direction: Optional[str] = None
    complexity: Optional[str] = None
    details: Optional[str] = None


class TextureProperties(BaseModel):
    visual_texture: Optional[str] = None
    tactile_texture: Optional[str] = None
    thickness_mm: Optional[float] = None
    surface_finish: Optional[str] = None


class StructuralElements(BaseModel):
    weave_type: Optional[str] = None
    stitching: Optional[str] = None
    reinforcements: List[str] = []
    details: List[str] = []


class StyleContext(BaseModel):
    intended_use: Optional[str] = None
    inspiration: Optional[str] = None
    historical_reference: Optional[str] = None


class FabricAnalysis(BaseModel):
    material_composition: MaterialComposition = Field(..., description="Material composition is required")
    color_palette: ColorPalette = Field(..., description="Color palette is required")
    pattern_characteristics: Optional[PatternCharacteristics] = None
    texture_properties: Optional[TextureProperties] = None
    structural_elements: Optional[StructuralElements] = None
    style_context: Optional[StyleContext] = None

FABRIC_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "material_composition": {
            "type": "OBJECT",
            "properties": {
                "primary_material": {"type": "STRING"},
                "blend_materials": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "material": {"type": "STRING"},
                            "percentage": {"type": "NUMBER"}
                        },
                        "required": ["material", "percentage"]
                    }
                },
                "notes": {"type": "STRING"}
            },
            "required": ["primary_material"]
        },
        "color_palette": {
            "type": "OBJECT",
            "properties": {
                "primary_color": {"type": "STRING"},
                "secondary_colors": {"type": "ARRAY", "items": {"type": "STRING"}},
                "accent_colors": {"type": "ARRAY", "items": {"type": "STRING"}},
                "hex_values": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "hex": {"type": "STRING"}
                        },
                        "required": ["name", "hex"]
                    }
                }
            },
            "required": ["primary_color"]
        },
        # add other properties as needed
    },
    "required": ["material_composition", "color_palette"]
}

