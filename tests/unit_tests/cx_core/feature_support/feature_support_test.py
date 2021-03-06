import pytest
from cx_core.feature_support import Features, FeatureSupport, SupportedFeatures
from cx_core.type_controller import TypeController


@pytest.mark.parametrize(
    "number, features, expected_supported_features",
    [
        (15, [1, 2, 4, 8, 16, 32, 64], {1, 2, 4, 8}),
        (16, [1, 2, 4, 8, 16, 32, 64], {16}),
        (31, [1, 2, 4, 8, 16, 64], {1, 2, 4, 8, 16}),
        (70, [1, 2, 4, 8, 16, 64], {2, 4, 64}),
    ],
)
def test_decode(
    number: int, features: Features, expected_supported_features: SupportedFeatures
):
    supported_features = FeatureSupport.decode(number, features)
    assert supported_features == expected_supported_features


@pytest.mark.parametrize(
    "supported_features, expected_number",
    [
        ({1, 2, 4, 8}, 15),
        ({16}, 16),
        ({1, 2, 4, 8, 16}, 31),
        ({2, 4, 64}, 70),
        ({1, 2, 4, 8, 16, 64}, 95),
    ],
)
def test_encode(supported_features: SupportedFeatures, expected_number: int):
    number = FeatureSupport.encode(supported_features)
    assert expected_number == number


@pytest.mark.parametrize(
    "number, features, feature, expected_is_supported",
    [
        (15, [1, 2, 4, 8, 16, 32, 64], 16, False),
        (16, [1, 2, 4, 8, 16, 32, 64], 2, False),
        (31, [1, 2, 4, 8, 16, 64], 64, False),
        (70, [1, 2, 4, 8, 16, 64], 4, True),
        (9, [1, 2, 4, 8, 16, 64], 8, True),
    ],
)
@pytest.mark.asyncio
async def test_is_supported(
    fake_type_controller: TypeController,
    number: int,
    features: Features,
    feature: int,
    expected_is_supported: bool,
):
    feature_support = FeatureSupport("fake_entity", fake_type_controller, False)
    feature_support.features = features
    feature_support._supported_features = FeatureSupport.decode(number, features)
    is_supported = await feature_support.is_supported(feature)
    assert is_supported == expected_is_supported


@pytest.mark.parametrize(
    "number, features, feature, expected_is_supported",
    [
        (15, [1, 2, 4, 8, 16, 32, 64], 16, True),
        (16, [1, 2, 4, 8, 16, 32, 64], 2, True),
        (31, [1, 2, 4, 8, 16, 64], 64, True),
        (70, [1, 2, 4, 8, 16, 64], 4, False),
        (9, [1, 2, 4, 8, 16, 64], 8, False),
    ],
)
@pytest.mark.asyncio
async def test_not_supported(
    fake_type_controller: TypeController,
    number: int,
    features: Features,
    feature: int,
    expected_is_supported: bool,
):
    feature_support = FeatureSupport("fake_entity", fake_type_controller, False)
    feature_support.features = features
    feature_support._supported_features = FeatureSupport.decode(number, features)
    is_supported = await feature_support.not_supported(feature)
    assert is_supported == expected_is_supported
