from pprint import pprint
import argparse
import datetime as dt
import boto3
import pandas as pd


def hello_world():
    return "hello world"


def get_params():
    parser = argparse.ArgumentParser(description="Print hello world")
    parser.add_argument(
        "--name", "-n", type=str, help="Name to greet", default="noname", required=False
    )
    return parser.parse_args()


def dsa(a):
    # a = set(a)
    # a = sorted(a,reverse=True)
    # a =set(sorted(tuple(a)))
    # print([x for k, v in a.items() if k == 'grain' and type(v) is dict for x in v.values() if type(x) is list])
    # print(['found none' for k,v in a.items() if isinstance(v, dict) for i,j in v.items() if j is None])
    # print(['found none' if j is None else 'None not found' for k, v in a.items() if isinstance(v, dict) for i, j in v.items()])
    # print([f'{k}.{i} is None' for k, v in a.items() if isinstance(v, dict) for i, j in v.items() if j is None])
    # print([f'{k}.{i} is None' if j is None else f'{k}.{i} is not None' for k, v in a.items() if isinstance(v, dict) for i, j in v.items()])
    # print(list(map(lambda x: x**3, filter(lambda x: x % 2 == 0, a))))
    # cub = lambda x: x**3
    # eve = lambda x: x % 2 == 0
    # print(list(map(cub, filter(eve, a))))
    # print([x**3 for x in a if x % 2 == 0])
    # print(all( x > 9 for x in a))
    # print(any( x < 9 for x in a))
    # keys = ['a', 'b', 'c']
    # values = [1, 2, 3]
    # pprint({k: v for k, v in zip(keys, values)})
    gen = (x**2 for x in a if x % 2 == 0)
    for x in gen:
        print(x)

    # return a
def filedemo():
    # without context manager
    f = open("Interview-prep/demo.txt", "w")
    f.write("Hello from filedemo!\n")
    f.close()

    # with context manager
    with open("Interview-prep/demo.txt", "a") as f:
        f.write("Hello from contextmanager filedemo!\n")

def create_vpc():
    ec2 = boto3.client("ec2", region_name="us-east-1")

    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]

    ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": "my-vpc"}])

    print(f"VPC created: {vpc_id}")
    return vpc_id



def main():
    args = get_params()
    pprint(f"hello_world {args.name[::-1]}")
    a = [1, 2, 4, 7, 2, 4, 8, 9, 4, 6, 7, 2, 9, 4]
    # a = {
    #     "fruit": {"name": "banana", "count": 3, "in_stock": True},
    #     "veggie": {"name": "carrot", "count": 10, "in_stock": False},
    #     "grain": {"name": "rice", "weight_kg": 2.5, "tags": ["organic", "whole"]},
    #     "dairy": {"name": "milk", "volume_ml": 500, "price": 1.99},
    #     "protein": {"name": "chicken", "weight_kg": 1.2, "in_stock": True},
    #     "spice": {"name": "pepper", "count": None, "tags": ["hot", "dry"]},
    # }
    # k = a.keys()
    # v = a.values()
    # print(k)
    # pprint(v)
    # pprint(dict(zip(k,v)))
    # print(dsa(a))
    dsa(a)
    filedemo()
    print(dt.datetime.now())
    print(dt.datetime.now().strftime("%B"))
    df = pd.read_csv("Interview-prep/data.csv")
    print(df.head(10))


if __name__ == "__main__":
    main()



"""
lambda - unnamed function, lambda <parameter variable>: logic
--------------------------------------------------------------------------------------------------------------------------------------
map() - Iterator, itrates over list and performs logic on all elements, 
         map(logic, variable(list))
--------------------------------------------------------------------------------------------------------------------------------------
filter() - Iterator, itrates over list and performs logic on all elements and returns list of elements which satisfy the condition/logic, 
         filter(logic, variable(list))
--------------------------------------------------------------------------------------------------------------------------------------
all() - performs AND operation and returns true/false
        all(<logic> for element in list-variable)
--------------------------------------------------------------------------------------------------------------------------------------
any() - performs OR operation and returns true/false
        any(<logic> for element in list-variable)
--------------------------------------------------------------------------------------------------------------------------------------
list comprihention - operation within list as per loops and conditions, returns modified list
        [x**2 for x in a if x%2]
--------------------------------------------------------------------------------------------------------------------------------------
dict comprihention - opretion within dict as per loops and conditions, returns modified dict
        {f'{k}_square', v**2} for k, v in x,items() if x % 2 == 0}
--------------------------------------------------------------------------------------------------------------------------------------
zip() - merge 2 differrnt list based on index key and value are generated for the dict
        k = [a,b,c]
        v = [1,2,3]
        zip(k,v) returns{a:1, b:2, c:3}
--------------------------------------------------------------------------------------------------------------------------------------
generator - special function which computes one element at a time, uses yeild(pause) insted of return and uses next function to itrate

        Generator expression — like list comprehension but with (): 
        gen = (x ** 2 for x in range(5))  # generator
        lst = [x ** 2 for x in range(5)]  # list

        def gen_squares(n):
            for x in range(n):
            yield x ** 2         # ← yield instead of return

        gen_squares(5)  # <generator object> ← nothing computed yet
        gen = gen_squares(5)
        next(gen)  # 0
        next(gen)  # 1
        next(gen)  # 4
        next(gen)  # 9
        next(gen)  # 16
        next(gen)  # StopIteration ← exhausted

        # or loop over it
        for x in gen_squares(5):
            print(x)  # 0, 1, 4, 9, 16
--------------------------------------------------------------------------------------------------------------------------------------
decorator is a wraper function which defines before and after functions. 
when used, passes function as a parameter to the generator/wrapper function

  def my_decorator(func):
      def wrapper():
          print("before")
          func()           # calls original function
          print("after")   
      return wrapper

  @my_decorator
  def greet():
      print("hello")

  greet()
  # before
  # hello
  # after

  @my_decorator is just shorthand for greet = my_decorator(greet).
//////////////////////////////////////////////////////////////////////////////////

  def bold(func):
      def wrapper():
          return "<b>" + func() + "</b>"
      return wrapper
  
  def italic(func):
      def wrapper():
          return "<i>" + func() + "</i>"
      return wrapper

  def underline(func):
      def wrapper():
          return "<u>" + func() + "</u>"
      return wrapper

  @bold
  @italic
  @underline
  def greet():
      return "hello"

  greet()  # <b><i><u>hello</u></i></b>

  ---
  Order matters — applied bottom up:
  @bold        # applied 3rd (outermost)
  @italic      # applied 2nd
  @underline   # applied 1st (innermost, closest to function)
  def greet():
      return "hello"
      
  # same as:
  greet = bold(italic(underline(greet)))
--------------------------------------------------------------------------------------------------------------------------------------
"""