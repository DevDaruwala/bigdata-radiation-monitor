import json
import pickle
from collections import deque

from src.flink_connect import kafka_streaming
from src.data_cleaning import clean_record


from pyflink.datastream import KeyedProcessFunction, RuntimeContext
from pyflink.common import Types
from pyflink.datastream.state import ValueStateDescriptor


# This class calculates:
# 1. Rolling average of last 30 radiation values for each country
# 2. Global running average across all countries

class CountryRollingAverage(KeyedProcessFunction):

    def open(self, runtime_context: RuntimeContext):
        self.runtime_context = runtime_context  # Flink's toolset

        # This will store last 30 values per country
        self.deque_state_desc = ValueStateDescriptor(
            "deque_state", Types.PICKLED_BYTE_ARRAY()
        )

        # These are global values shared by all records
        self.global_sum_desc = ValueStateDescriptor("global_sum", Types.FLOAT())
        self.global_count_desc = ValueStateDescriptor("global_count", Types.LONG())

    def process_element(self, value, ctx):
        try:
            # Extract country and value from input
            country = value.get('country', 'Unknown')
            val_str = value.get('Value')

            if val_str is None:
                print(json.dumps({'error': 'Missing Value'}))
                return

            val = float(val_str)

            # ───── Country Rolling Average ─────
            deque_state = self.runtime_context.get_state(self.deque_state_desc)
            dq = pickle.loads(deque_state.value()) if deque_state.value() else deque(maxlen=30)

            dq.append(val)  # Add latest reading
            deque_state.update(pickle.dumps(dq))

            country_avg = sum(dq) / len(dq)
            country_count = len(dq)

            # ───── Global Running Average ─────
            global_sum_state = self.runtime_context.get_state(self.global_sum_desc)
            global_count_state = self.runtime_context.get_state(self.global_count_desc)

            total_sum = global_sum_state.value() if global_sum_state.value() else 0.0
            total_count = global_count_state.value() if global_count_state.value() else 0

            total_sum += val
            total_count += 1

            global_sum_state.update(total_sum)
            global_count_state.update(total_count)

            global_avg = total_sum / total_count

            # This is final output
            result = {
                'country': country,
                'average': round(country_avg, 2),
                'count': country_count,
                'global_average': round(global_avg, 2),
                #'global_count': total_count
            }

            print(json.dumps(result))

        except Exception as e:
            print(json.dumps({'error': str(e)}))


# This is your Flink main pipeline function

def rolling_average():
    env, data_stream = kafka_streaming()  # get stream & environment

    cleaned_stream = data_stream \
        .map(lambda record: clean_record(json.loads(record)),
             output_type=Types.MAP(Types.STRING(), Types.STRING())) \
        .filter(lambda x: x is not None)

    # Group data by country and apply our custom processor
    cleaned_stream \
        .key_by(lambda x: x['country']) \
        .process(CountryRollingAverage())

    env.execute("Per-Country and Global Rolling Average")


if __name__ == "__main__":
    print("Starting Flink job for rolling averages...")
    rolling_average()
