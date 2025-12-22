#!/usr/bin/env python
"""
Populate Dummy Blogs Script

This script creates dummy categories and blog posts for testing and development.
Run this script from the Django project root directory.

Usage:
    python populate_blogs.py [--blogs=20] [--categories=5] [--clear]

Options:
    --blogs=N         Number of blog posts to create (default: 20)
    --categories=N    Number of categories to create (default: 5)
    --clear           Delete all existing blogs and categories before creating new ones
    --help            Show this help message

Examples:
    python populate_blogs.py
    python populate_blogs.py --blogs=50 --categories=10
    python populate_blogs.py --clear --blogs=30
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils.text import slugify
from django.core.files.base import ContentFile
from blog.models import Blog, Category
from PIL import Image
import io


# Sample data
CATEGORIES_DATA = [
    {
        'name': 'Technology',
        'description': 'Latest trends and innovations in technology, software development, and digital transformation.'
    },
    {
        'name': 'Business',
        'description': 'Business strategies, entrepreneurship, and corporate insights for modern professionals.'
    },
    {
        'name': 'Lifestyle',
        'description': 'Tips and inspiration for better living, health, wellness, and personal development.'
    },
    {
        'name': 'Travel',
        'description': 'Explore destinations, travel tips, and adventures from around the world.'
    },
    {
        'name': 'Food & Cooking',
        'description': 'Delicious recipes, cooking techniques, and culinary adventures for food lovers.'
    },
    {
        'name': 'Design',
        'description': 'Creative design inspiration, UI/UX trends, and visual storytelling.'
    },
    {
        'name': 'Marketing',
        'description': 'Digital marketing strategies, SEO tips, and content marketing best practices.'
    },
    {
        'name': 'Finance',
        'description': 'Personal finance, investment strategies, and economic insights.'
    },
    {
        'name': 'Education',
        'description': 'Learning resources, educational technology, and academic insights.'
    },
    {
        'name': 'Health & Fitness',
        'description': 'Fitness routines, nutrition advice, and wellness tips for a healthier lifestyle.'
    },
]

BLOG_TITLES = {
    'Technology': [
        'The Future of Artificial Intelligence in 2025',
        '10 Programming Languages Every Developer Should Learn',
        'Cloud Computing: A Comprehensive Guide for Beginners',
        'Cybersecurity Best Practices for Modern Businesses',
        'The Rise of Quantum Computing: What You Need to Know',
        'Web Development Trends That Will Dominate This Year',
        'Machine Learning vs Deep Learning: Understanding the Difference',
        'Building Scalable Microservices Architecture',
        'The Complete Guide to DevOps Practices',
        'Blockchain Technology Beyond Cryptocurrency',
    ],
    'Business': [
        'How to Build a Successful Startup from Scratch',
        'Remote Work: Strategies for Managing Distributed Teams',
        'The Art of Negotiation in Business Deals',
        'Digital Transformation: A Step-by-Step Guide',
        'Leadership Skills Every Manager Should Master',
        'Creating a Winning Business Plan in 2025',
        'The Power of Networking in Business Growth',
        'Effective Time Management for Entrepreneurs',
        'Understanding Your Target Market: A Complete Guide',
        'Scaling Your Business: When and How to Grow',
    ],
    'Lifestyle': [
        '10 Daily Habits That Will Transform Your Life',
        'Minimalism: The Art of Living with Less',
        'Work-Life Balance: Finding Your Perfect Equilibrium',
        'Morning Routines of Highly Successful People',
        'The Ultimate Guide to Mindfulness and Meditation',
        'Sustainable Living: Small Changes, Big Impact',
        'Productivity Hacks for Busy Professionals',
        'The Science of Happiness: What Really Makes Us Happy',
        'Digital Detox: Reclaiming Your Time and Attention',
        'Building Better Relationships in the Modern World',
    ],
    'Travel': [
        'Top 10 Hidden Gems in Southeast Asia',
        'Solo Travel: A Complete Guide for First-Timers',
        'Budget Travel Tips: See the World Without Breaking the Bank',
        'The Ultimate European Backpacking Itinerary',
        'Digital Nomad Life: Working While Traveling',
        'Sustainable Tourism: How to Travel Responsibly',
        'Adventure Travel: Thrilling Destinations for Adrenaline Junkies',
        'Cultural Immersion: Experiencing Local Life Abroad',
        'Travel Photography: Capturing Your Adventures',
        'The Best Food Destinations Around the World',
    ],
    'Food & Cooking': [
        '30-Minute Meals: Quick and Delicious Recipes',
        'The Art of Baking: From Beginner to Expert',
        'Plant-Based Cooking: Delicious Vegan Recipes',
        'Mastering the Basics: Essential Cooking Techniques',
        'International Cuisine: A Culinary Journey',
        'Meal Prep 101: Save Time and Eat Healthy',
        'The Science of Flavor: Understanding Taste Combinations',
        'Cooking with Seasonal Ingredients',
        'Desserts That Will Impress Your Guests',
        'Kitchen Gadgets Every Home Cook Needs',
    ],
}

LOREM_PARAGRAPHS = [
    "In today's rapidly evolving landscape, staying ahead of the curve requires continuous learning and adaptation. This comprehensive guide will walk you through everything you need to know to master this subject and apply it effectively in real-world scenarios.",
    
    "Whether you're a complete beginner or looking to refine your existing skills, this article provides valuable insights and practical tips that you can implement immediately. We've compiled years of experience and research into this definitive resource.",
    
    "The key to success lies in understanding the fundamental principles and building upon them systematically. Throughout this guide, we'll explore various strategies, techniques, and best practices that have proven effective time and time again.",
    
    "One of the most important aspects to consider is the balance between theory and practice. While understanding the concepts is crucial, applying them in real situations is where true mastery develops. We'll provide numerous examples and case studies to illustrate these points.",
    
    "As we delve deeper into this topic, you'll discover that success often comes from attention to detail and consistent effort. Small improvements compound over time, leading to significant results that can transform your approach and outcomes.",
    
    "The landscape is constantly changing, which means staying informed about the latest trends and developments is essential. We'll explore current best practices while also looking ahead to emerging trends that will shape the future.",
    
    "Collaboration and community play a vital role in growth and development. By connecting with others who share your interests and goals, you can accelerate your learning and gain perspectives that you might not have considered otherwise.",
    
    "Remember that everyone's journey is unique, and what works for one person may not work for another. The key is to experiment, learn from your experiences, and continuously refine your approach based on what you discover.",
]


def create_thumbnail(width=800, height=450, color=None):
    """Create a simple colored thumbnail image"""
    if color is None:
        color = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )
    
    img = Image.new('RGB', (width, height), color=color)
    
    # Save to BytesIO
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=85)
    img_io.seek(0)
    
    return ContentFile(img_io.read(), name='thumbnail.jpg')


def generate_content(num_paragraphs=5):
    """Generate blog content from lorem paragraphs"""
    paragraphs = random.sample(LOREM_PARAGRAPHS, min(num_paragraphs, len(LOREM_PARAGRAPHS)))
    
    # Add some HTML formatting
    content = ""
    for i, para in enumerate(paragraphs):
        if i == 0:
            content += f"<h2>Introduction</h2>\n<p>{para}</p>\n\n"
        elif i == len(paragraphs) - 1:
            content += f"<h2>Conclusion</h2>\n<p>{para}</p>\n"
        else:
            content += f"<p>{para}</p>\n\n"
    
    return content


def create_categories(num_categories=5, clear=False):
    """Create sample categories"""
    if clear:
        print("🗑️  Clearing existing categories...")
        Category.objects.all().delete()
        print("✅ Categories cleared")
    
    print(f"\n📁 Creating {num_categories} categories...")
    
    categories = []
    category_data = random.sample(CATEGORIES_DATA, min(num_categories, len(CATEGORIES_DATA)))
    
    for data in category_data:
        slug = slugify(data['name'])
        category, created = Category.objects.get_or_create(
            slug=slug,
            defaults={
                'name': data['name'],
                'description': data['description']
            }
        )
        
        if created:
            print(f"  ✓ Created category: {category.name}")
        else:
            print(f"  ⚠ Category already exists: {category.name}")
        
        categories.append(category)
    
    return categories


def create_blogs(num_blogs=20, categories=None, clear=False):
    """Create sample blog posts"""
    if clear:
        print("\n🗑️  Clearing existing blogs...")
        Blog.objects.all().delete()
        print("✅ Blogs cleared")
    
    if not categories:
        categories = list(Category.objects.all())
        if not categories:
            print("❌ No categories found. Creating default categories first...")
            categories = create_categories()
    
    print(f"\n📝 Creating {num_blogs} blog posts...")
    
    created_count = 0
    skipped_count = 0
    
    for i in range(num_blogs):
        # Select random category
        category = random.choice(categories)
        
        # Get titles for this category
        category_titles = BLOG_TITLES.get(category.name, [
            f"Interesting Article About {category.name} #{i+1}",
            f"Deep Dive into {category.name} #{i+1}",
            f"Everything You Need to Know About {category.name} #{i+1}",
        ])
        
        # Select random title
        if category_titles:
            title = random.choice(category_titles)
            # Remove used title to avoid duplicates
            category_titles.remove(title)
        else:
            title = f"{category.name} Article #{i+1}"
        
        # Generate slug
        slug = slugify(title)
        
        # Check if blog already exists
        if Blog.objects.filter(slug=slug).exists():
            print(f"  ⚠ Blog already exists: {title}")
            skipped_count += 1
            continue
        
        # Generate content
        short_description = random.choice(LOREM_PARAGRAPHS)[:200] + "..."
        content = generate_content(random.randint(4, 7))
        
        # Random publish status (80% published)
        is_published = random.random() < 0.8
        
        # Create thumbnail
        thumbnail = create_thumbnail()
        
        # Create blog
        blog = Blog.objects.create(
            title=title,
            slug=slug,
            short_description=short_description,
            content=content,
            category=category,
            is_published=is_published,
        )
        
        # Save thumbnail
        blog.thumbnail.save(f'blog_{blog.id}.jpg', thumbnail, save=True)
        
        # Randomly adjust created_at date (within last 90 days)
        days_ago = random.randint(0, 90)
        blog.created_at = datetime.now() - timedelta(days=days_ago)
        blog.save()
        
        status = "✓ Published" if is_published else "○ Draft"
        print(f"  {status} {title} ({category.name})")
        created_count += 1
    
    print(f"\n✅ Created {created_count} blogs")
    if skipped_count > 0:
        print(f"⚠️  Skipped {skipped_count} duplicate blogs")


def show_stats():
    """Show database statistics"""
    print("\n" + "="*60)
    print("📊 DATABASE STATISTICS")
    print("="*60)
    
    total_categories = Category.objects.count()
    total_blogs = Blog.objects.count()
    published_blogs = Blog.objects.filter(is_published=True).count()
    draft_blogs = Blog.objects.filter(is_published=False).count()
    
    print(f"\n📁 Categories: {total_categories}")
    print(f"📝 Total Blogs: {total_blogs}")
    print(f"  ✓ Published: {published_blogs}")
    print(f"  ○ Drafts: {draft_blogs}")
    
    print("\n📁 Blogs per Category:")
    for category in Category.objects.all():
        count = category.blogs.count()
        published = category.blogs.filter(is_published=True).count()
        print(f"  {category.name}: {count} total ({published} published)")
    
    print("\n" + "="*60)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Populate database with dummy blogs and categories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--blogs', type=int, default=20, help='Number of blogs to create (default: 20)')
    parser.add_argument('--categories', type=int, default=5, help='Number of categories to create (default: 5)')
    parser.add_argument('--clear', action='store_true', help='Clear existing data before creating new')
    
    args = parser.parse_args()
    
    print("="*60)
    print("🚀 BLOG POPULATION SCRIPT")
    print("="*60)
    
    try:
        # Create categories
        categories = create_categories(args.categories, clear=args.clear)
        
        # Create blogs
        create_blogs(args.blogs, categories, clear=args.clear)
        
        # Show statistics
        show_stats()
        
        print("\n✅ Script completed successfully!")
        print("\n💡 You can now view your blogs at:")
        print("   - API: http://localhost:8000/api/blogs/")
        print("   - Admin: http://localhost:8000/admin/blog/blog/")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
