import random
from data import DatabaseManager, ActorRank
from logger import Logger

class TheaterController:
    def __init__(self):
        self.db = DatabaseManager()
        self.logger = Logger()
        self.is_connected = False

    def connect_to_database(self):
        self.is_connected = self.db.connect()
        return self.is_connected

    def initialize_database(self):
        result1 = self.db.create_schema()
        result2 = self.db.init_sample_data()
        return result1 and result2

    def reset_database(self):
        return self.db.reset_database()

    def get_game_state(self):
        return self.db.get_game_data()

    def get_all_actors(self):
        return self.db.get_actors()

    def get_all_plots(self):
        return self.db.get_plots()

    def get_performances_history(self):
        return self.db.get_performances()

    def get_performance_details(self, performance_id):
        performances = self.db.get_performances()
        performance = next((p for p in performances if p['performance_id'] == performance_id), None)

        if not performance:
            return None

        actors = self.db.get_actors_in_performance(performance_id)

        return {
            'performance': performance,
            'actors': actors
        }

    def create_new_performance(self, title, plot_id, year, budget):
        game_data = self.db.get_game_data()
        if game_data['capital'] < budget:
            return False, "Недостаточно средств в капитале"

        plots = self.db.get_plots()
        plot = next((p for p in plots if p['plot_id'] == plot_id), None)

        if not plot:
            return False, "Сюжет не найден"

        if budget < plot['minimum_budget']:
            return False, "Бюджет меньше минимально необходимого для данного сюжета"

        performance_id = self.db.create_performance(title, plot_id, year, budget)

        if performance_id:
            new_capital = game_data['capital'] - budget
            self.db.update_game_data(year, new_capital)
            return True, performance_id
        else:
            return False, "Ошибка при создании спектакля"

    def assign_actor_to_performance(self, actor_id, performance_id, role, contract_cost):
        return self.db.assign_actor_to_role(actor_id, performance_id, role, contract_cost)

    def calculate_contract_cost(self, actor):
        base_cost = 30000

        rank_order = ['Начинающий', 'Постоянный', 'Ведущий', 'Мастер', 'Заслуженный', 'Народный']
        rank_bonus = rank_order.index(actor['rank']) * 10000

        experience_bonus = actor['experience'] * 2000
        awards_bonus = actor['awards_count'] * 5000

        contract_cost = base_cost + rank_bonus + experience_bonus + awards_bonus

        premium = contract_cost / 5

        return {
            'contract': contract_cost,
            'premium': premium,
            'total': contract_cost + premium
        }

    def calculate_performance_result(self, performance_id):
        performances = self.db.get_performances()
        performance = next((p for p in performances if p['performance_id'] == performance_id), None)

        if not performance or performance['is_completed']:
            return False, "Спектакль не найден или уже завершен"

        plots = self.db.get_plots()
        plot = next((p for p in plots if p['plot_id'] == performance['plot_id']), None)

        actors = self.db.get_actors_in_performance(performance_id)

        total_spent = plot['production_cost']
        for actor in actors:
            total_spent += actor['contract_cost']

        actual_budget = min(performance['budget'], total_spent)
        saved_budget = performance['budget'] - actual_budget

        base_revenue = actual_budget * (0.8 + 0.1 * plot['demand'])

        actors_bonus = 0
        for actor in actors:
            rank_order = ['Начинающий', 'Постоянный', 'Ведущий', 'Мастер', 'Заслуженный', 'Народный']
            rank_multiplier = 1 + (rank_order.index(actor['rank']) * 0.1)

            award_bonus = actor['awards_count'] * 0.05
            exp_bonus = actor['experience'] * 0.01

            actor_contribution = actor['contract_cost'] * rank_multiplier * (1 + award_bonus + exp_bonus)
            actors_bonus += actor_contribution

        random_factor = random.uniform(0.9, 1.1)

        total_revenue = int((base_revenue + actors_bonus) * random_factor)

        profit = total_revenue - actual_budget

        self.db.update_performance_budget(performance_id, actual_budget)

        self.db.complete_performance(performance_id, total_revenue)

        game_data = self.db.get_game_data()
        new_capital = game_data['capital'] + profit + saved_budget
        current_year = game_data['current_year'] + 1
        self.db.update_game_data(current_year, new_capital)

        successful_actors = []
        if profit > 0:
            rank_order = ['Начинающий', 'Постоянный', 'Ведущий', 'Мастер', 'Заслуженный', 'Народный']
            sorted_actors = sorted(actors,
                               key=lambda a: (rank_order.index(a['rank']),
                                              a['experience'],
                                              a['awards_count']),
                               reverse=True)

            for i, actor in enumerate(sorted_actors[:3]):
                self.db.award_actor(actor['actor_id'])
                successful_actors.append(actor)

                if i == 0 and profit > actual_budget * 0.5:
                    self.db.upgrade_actor_rank(actor['actor_id'])

        return True, {
            'revenue': total_revenue,
            'budget': actual_budget,
            'original_budget': performance['budget'],
            'saved_budget': saved_budget,
            'profit': profit,
            'awarded_actors': successful_actors
        }

    def skip_year(self):
        game_data = self.db.get_game_data()
        current_year = game_data['current_year']
        current_capital = game_data['capital']

        rights_sale = int(current_capital * random.uniform(0.1, 0.2))

        new_capital = current_capital + rights_sale
        new_year = current_year + 1

        self.db.update_game_data(new_year, new_capital)

        return {
            'year': new_year,
            'capital': new_capital,
            'rights_sale': rights_sale
        }

    def add_new_actor(self, last_name, first_name, patronymic, rank, awards_count, experience):
        return self.db.add_actor(last_name, first_name, patronymic, rank, awards_count, experience)

    def delete_actor_by_id(self, actor_id):
        return self.db.delete_actor(actor_id)

    def close(self):
        self.db.disconnect()