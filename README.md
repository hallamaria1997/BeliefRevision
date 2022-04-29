# BeliefRevision
Implementation for project 2 in the course Introduction to AI. Code compiles and runs on python 3.8 and a macOS system. 

# Requirements
Run the following statement to install all the requirements: 

```python
pip install -r requirements.txt
```

# How to run the code
Run the following command to execute the belief revision: 

```python
python cli.py
```

Now, you will see five different actions: 

```
1. Display belief base: to display the belief base 
2. Add to belief base: to add a belief to the belief base
3. Clear belief base: to clear the belief base
4. Check entailment: to check if a belief is true or false in the belief base
5. Quit: to quit the program
```

You can use the following symbols in the belief base: 

```
& : and
| : or
>> : implies
<> : biconditional
~ : not
```

# How to run the tests
```python
python -m pytest test.py
```

# How to get the test coverage

```python
pytest --cov=. test.py
```