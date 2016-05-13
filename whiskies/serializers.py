from django.contrib.auth.models import User
from rest_framework import serializers


from whiskies.models import Whiskey, Profile, Review, TagSearch, Tag,\
    TagTracker


class ProfileSerializer(serializers.ModelSerializer):

    # check that liked and disliked whiskies are displayed

    class Meta:
        model = Profile
        fields = ("user", "liked_whiskies", "disliked_whiskies")


class UserSerializer(serializers.ModelSerializer):

    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tag_searches = serializers.PrimaryKeyRelatedField(many=True,
                                                      read_only=True)

    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    whiskey_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "tag_searches", "reviews",
                  "profile", "whiskey_id")


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    whiskey = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    #whiskies = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tag
        fields = ("title",)


class TagSearchSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    search_string = serializers.CharField()

    class Meta:
        model = TagSearch
        fields = "__all__"


class TagTrackerSerializer(serializers.ModelSerializer):

    title = serializers.ReadOnlyField(source='tag.title')

    class Meta:
        model = TagTracker
        fields = ("title", "count")


class CompWhiskeySerializer(serializers.ModelSerializer):
    """
    For displaying comparable whiskies on the Whiskey model.
    """

    class Meta:
        model = Whiskey
        fields = ("id", "title", "img_url", "rating", "price", "region")


class WhiskeySerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    tags = TagTrackerSerializer(source="tagtracker_set", many=True)
    comparables = CompWhiskeySerializer(many=True, read_only=True)

    class Meta:
        model = Whiskey
        fields = ("id", "title", "img_url", "region", "price", "rating",
                  "description", "reviews", "comparables", "comparable", "tags")


class AddLikedSerializer(serializers.Serializer):
    """
    For updating a profiles liked/disliked whiskies.
    """

    whiskey_id = serializers.IntegerField(read_only=True)
    action = serializers.CharField(read_only=True)
    opinion = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):

        instance.profile.update_likes(**validated_data)

        return instance
