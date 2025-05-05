from flask import jsonify, request, render_template
from queue import Queue
import threading
from .telegram_monitor import TelegramMonitor

results_queue = Queue()
monitor = TelegramMonitor()

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/search', methods=['POST'])
    def search():
        data = request.get_json()
        monitor.start_monitoring(
            data['company_name'],
            data['keywords'],
            results_queue
        )
        return jsonify({"success": True})
    
    @app.route('/api/results', methods=['GET'])
    def get_results():
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        return jsonify({"results": results})