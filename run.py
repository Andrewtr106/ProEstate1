from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting ProEstate Real Estate Website...")
    print("=" * 60)
    print("📍 Website URL: http://localhost:5000")
    print("📍 Admin Panel: http://localhost:5000/admin/add-property")
    print("📍 Properties: http://localhost:5000/properties")
    print("📍 Contact: http://localhost:5000/contact")
    print("=" * 60)
    print("⚡ Server is running...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)