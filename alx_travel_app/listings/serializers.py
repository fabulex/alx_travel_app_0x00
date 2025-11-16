from rest_framework import serializers
from .models import Listing, Booking, Review, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_host']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # Simple for reviews; add nesting if needed

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'  # Includes all, but overrides for nesting
        read_only_fields = ['id', 'created_at', 'total_price']

    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in.")
        return data

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'  # All fields, with overrides for nesting
        read_only_fields = ['id', 'created_at', 'updated_at', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.bookings.filter(review__isnull=False).values_list('review__rating', flat=True)
        return round(sum(reviews) / len(reviews), 1) if reviews else 0
