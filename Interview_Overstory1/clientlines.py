class ClientLines(SchemaModel):
    """
    Client Lines dataset
    """

    geometry: Series[gpd.array.GeometryDtype]
    level3: Series[str] = Field(unique=True, description="Unique line ID")
    level1: Optional[Series[str]] = Field(nullable=True)
    level2: Optional[Series[str]] = Field(nullable=True)
    phasingType: Optional[Series[str]] = Field(
        isin=["single-phase", "two-phase", "three-phase"], nullable=True
    )

    class Config:
        name = "Client lines"
        description = "Cleaned client lines dataset"
        unique_column_names = True

    @check("geometry", name="geometry_is_valid")
    def geometry_is_valid(cls, geom: Series[gpd.array.GeometryDtype]) -> Series[bool]:
        return geom.is_valid

    @check("geometry", name="geometry_is_linestring")
    def geometry_is_linestring(
        cls, geom: Series[gpd.array.GeometryDtype]
    ) -> Series[bool]:
        return geom.geom_type == "LineString"

    @dataframe_check
    def dataframe_in_utm(cls, gdf: gpd.GeoDataFrame) -> Series[bool]:
        """Ensure dataframe CRS is in UTM"""
        return gdf.estimate_utm_crs() == gdf.crs
    



MIN_LINE_LENGTH_IN_M = 2  # Default minimum span length

def validate(gdf: gpd.GeoDataFrame, schema):
    try:
        return schema.validate(gdf, lazy=True)
    except pa.errors.SchemaErrors as err:
        logger.error(err.failure_cases)

def validate_client_poles(gdf: gpd.GeoDataFrame):
    try:
        return ClientPoles.validate(gdf, lazy=True)
    except pa.errors.SchemaErrors as err:
        logger.error(err.failure_cases)
        assert False, "Validation failed."


def validate_client_lines(
    gdf: gpd.GeoDataFrame, min_line_length_in_m: float = MIN_LINE_LENGTH_IN_M
):
    try:
        geometry_column = pa.Column(
            gpd.array.GeometryDtype,
            name="geometry",
            checks=pa.Check(
                lambda x: x.length > min_line_length_in_m,
                error="Line should meet minimum line length.",
                name="geometry_min_length",
            ),
        )
        geometry_column.validate(gdf, lazy=True)
        return ClientLines.validate(gdf, lazy=True)
    except pa.errors.SchemaErrors as err:
        logger.error(err.failure_cases)
        assert False, "Validation failed."