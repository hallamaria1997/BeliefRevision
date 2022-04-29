from agent import Agent
from belief import Belief
from beliefbase import BeliefBase
from sympy.logic.boolalg import to_cnf, Not

def test_revision():
    """ Test if revision works correctly in the belief base """
    agent = Agent()
    agent.belief_base.add('p')
    agent.belief_base.add('q')
    agent.belief_base.add('p>>q')
    assert len(agent.belief_base.beliefBase.keys()) == 3
    agent.belief_base.add('~q')
    assert len(agent.belief_base.beliefBase.keys()) == 2

def test_contraction():
    """ Test if contraction works correcly in the belief base """
    agent = Agent()
    agent.belief_base.add('p')
    agent.belief_base.add('~q')
    agent.belief_base.contract('~q', 'q')
    assert len(agent.belief_base.beliefBase.keys()) == 1

def test_expansion():
    """ Test if by expanding a belief it gets added to the belief base """
    agent = Agent()
    assert len(agent.belief_base.beliefBase.keys()) == 0
    agent.belief_base.expand('p')
    assert len(agent.belief_base.beliefBase.keys()) == 1

def test_vacuity():
    """ Test that if a belief is contracted from the belief base but did not already exist, nothing happens """
    agent = Agent()
    agent.belief_base.add('p')
    agent.belief_base.add('q')
    agent.belief_base.add('p>>q')
    assert len(agent.belief_base.beliefBase.keys()) == 3
    agent.belief_base.contract('r', '~r')
    assert len(agent.belief_base.beliefBase.keys()) == 3

def test_extentionality():
    """ Test resolution """
    agent = Agent()
    agent.belief_base.add('p')
    agent.belief_base.add('q')
    agent.belief_base.add('q<>p')
    assert agent.belief_base.pl_resolution('(p>>q)&(q>>p)') == True

def test_consistency():
    """ Make a few different cases to check for consistency """
    agent = Agent()
    agent.belief_base.add('p')
    agent.belief_base.add('q')
    agent.belief_base.add('(p&q)>>r')
    agent.belief_base.add('~r')
    assert len(agent.belief_base.beliefBase.keys()) == 1

    agent.belief_base.clear()
    agent.belief_base.add('p')
    agent.belief_base.add('~p')
    assert len(agent.belief_base.beliefBase.keys()) == 1

    agent.belief_base.clear()
    agent.belief_base.add('(p|q)&(p&q)')
    agent.belief_base.add('~p')
    assert len(agent.belief_base.beliefBase.keys()) == 1