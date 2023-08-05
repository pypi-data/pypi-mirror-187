# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: unified_planning.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16unified_planning.proto\"i\n\nExpression\x12\x13\n\x04\x61tom\x18\x01 \x01(\x0b\x32\x05.Atom\x12\x19\n\x04list\x18\x02 \x03(\x0b\x32\x0b.Expression\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x1d\n\x04kind\x18\x04 \x01(\x0e\x32\x0f.ExpressionKind\"\\\n\x04\x41tom\x12\x10\n\x06symbol\x18\x01 \x01(\tH\x00\x12\r\n\x03int\x18\x02 \x01(\x03H\x00\x12\x15\n\x04real\x18\x03 \x01(\x0b\x32\x05.RealH\x00\x12\x11\n\x07\x62oolean\x18\x04 \x01(\x08H\x00\x42\t\n\x07\x63ontent\".\n\x04Real\x12\x11\n\tnumerator\x18\x01 \x01(\x03\x12\x13\n\x0b\x64\x65nominator\x18\x02 \x01(\x03\"9\n\x0fTypeDeclaration\x12\x11\n\ttype_name\x18\x01 \x01(\t\x12\x13\n\x0bparent_type\x18\x02 \x01(\t\"\'\n\tParameter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"n\n\x06\x46luent\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nvalue_type\x18\x02 \x01(\t\x12\x1e\n\nparameters\x18\x03 \x03(\x0b\x32\n.Parameter\x12\"\n\rdefault_value\x18\x04 \x01(\x0b\x32\x0b.Expression\"/\n\x11ObjectDeclaration\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"\xcd\x01\n\x10\x45\x66\x66\x65\x63tExpression\x12*\n\x04kind\x18\x01 \x01(\x0e\x32\x1c.EffectExpression.EffectKind\x12\x1b\n\x06\x66luent\x18\x02 \x01(\x0b\x32\x0b.Expression\x12\x1a\n\x05value\x18\x03 \x01(\x0b\x32\x0b.Expression\x12\x1e\n\tcondition\x18\x04 \x01(\x0b\x32\x0b.Expression\"4\n\nEffectKind\x12\n\n\x06\x41SSIGN\x10\x00\x12\x0c\n\x08INCREASE\x10\x01\x12\x0c\n\x08\x44\x45\x43REASE\x10\x02\"M\n\x06\x45\x66\x66\x65\x63t\x12!\n\x06\x65\x66\x66\x65\x63t\x18\x01 \x01(\x0b\x32\x11.EffectExpression\x12 \n\x0foccurrence_time\x18\x02 \x01(\x0b\x32\x07.Timing\"C\n\tCondition\x12\x19\n\x04\x63ond\x18\x01 \x01(\x0b\x32\x0b.Expression\x12\x1b\n\x04span\x18\x02 \x01(\x0b\x32\r.TimeInterval\"\x8d\x01\n\x06\x41\x63tion\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1e\n\nparameters\x18\x02 \x03(\x0b\x32\n.Parameter\x12\x1b\n\x08\x64uration\x18\x03 \x01(\x0b\x32\t.Duration\x12\x1e\n\nconditions\x18\x04 \x03(\x0b\x32\n.Condition\x12\x18\n\x07\x65\x66\x66\x65\x63ts\x18\x05 \x03(\x0b\x32\x07.Effect\"\x90\x01\n\tTimepoint\x12&\n\x04kind\x18\x01 \x01(\x0e\x32\x18.Timepoint.TimepointKind\x12\x14\n\x0c\x63ontainer_id\x18\x02 \x01(\t\"E\n\rTimepointKind\x12\x10\n\x0cGLOBAL_START\x10\x00\x12\x0e\n\nGLOBAL_END\x10\x01\x12\t\n\x05START\x10\x02\x12\x07\n\x03\x45ND\x10\x03\"=\n\x06Timing\x12\x1d\n\ttimepoint\x18\x01 \x01(\x0b\x32\n.Timepoint\x12\x14\n\x05\x64\x65lay\x18\x02 \x01(\x0b\x32\x05.Real\"o\n\x08Interval\x12\x14\n\x0cis_left_open\x18\x01 \x01(\x08\x12\x1a\n\x05lower\x18\x02 \x01(\x0b\x32\x0b.Expression\x12\x15\n\ris_right_open\x18\x03 \x01(\x08\x12\x1a\n\x05upper\x18\x04 \x01(\x0b\x32\x0b.Expression\"k\n\x0cTimeInterval\x12\x14\n\x0cis_left_open\x18\x01 \x01(\x08\x12\x16\n\x05lower\x18\x02 \x01(\x0b\x32\x07.Timing\x12\x15\n\ris_right_open\x18\x03 \x01(\x08\x12\x16\n\x05upper\x18\x04 \x01(\x0b\x32\x07.Timing\"5\n\x08\x44uration\x12)\n\x16\x63ontrollable_in_bounds\x18\x01 \x01(\x0b\x32\t.Interval\"G\n\x17\x41\x62stractTaskDeclaration\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1e\n\nparameters\x18\x02 \x03(\x0b\x32\n.Parameter\"F\n\x04Task\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\ttask_name\x18\x02 \x01(\t\x12\x1f\n\nparameters\x18\x03 \x03(\x0b\x32\x0b.Expression\"\xaf\x01\n\x06Method\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1e\n\nparameters\x18\x02 \x03(\x0b\x32\n.Parameter\x12\x1c\n\rachieved_task\x18\x03 \x01(\x0b\x32\x05.Task\x12\x17\n\x08subtasks\x18\x04 \x03(\x0b\x32\x05.Task\x12 \n\x0b\x63onstraints\x18\x05 \x03(\x0b\x32\x0b.Expression\x12\x1e\n\nconditions\x18\x06 \x03(\x0b\x32\n.Condition\"g\n\x0bTaskNetwork\x12\x1d\n\tvariables\x18\x01 \x03(\x0b\x32\n.Parameter\x12\x17\n\x08subtasks\x18\x02 \x03(\x0b\x32\x05.Task\x12 \n\x0b\x63onstraints\x18\x03 \x03(\x0b\x32\x0b.Expression\"\x83\x01\n\tHierarchy\x12\x30\n\x0e\x61\x62stract_tasks\x18\x01 \x03(\x0b\x32\x18.AbstractTaskDeclaration\x12\x18\n\x07methods\x18\x02 \x03(\x0b\x32\x07.Method\x12*\n\x14initial_task_network\x18\x03 \x01(\x0b\x32\x0c.TaskNetwork\"@\n\x04Goal\x12\x19\n\x04goal\x18\x01 \x01(\x0b\x32\x0b.Expression\x12\x1d\n\x06timing\x18\x02 \x01(\x0b\x32\r.TimeInterval\"R\n\x0bTimedEffect\x12!\n\x06\x65\x66\x66\x65\x63t\x18\x01 \x01(\x0b\x32\x11.EffectExpression\x12 \n\x0foccurrence_time\x18\x02 \x01(\x0b\x32\x07.Timing\"E\n\nAssignment\x12\x1b\n\x06\x66luent\x18\x01 \x01(\x0b\x32\x0b.Expression\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.Expression\">\n\x0cGoalWithCost\x12\x19\n\x04goal\x18\x01 \x01(\x0b\x32\x0b.Expression\x12\x13\n\x04\x63ost\x18\x02 \x01(\x0b\x32\x05.Real\"\xd0\x03\n\x06Metric\x12 \n\x04kind\x18\x01 \x01(\x0e\x32\x12.Metric.MetricKind\x12\x1f\n\nexpression\x18\x02 \x01(\x0b\x32\x0b.Expression\x12.\n\x0c\x61\x63tion_costs\x18\x03 \x03(\x0b\x32\x18.Metric.ActionCostsEntry\x12(\n\x13\x64\x65\x66\x61ult_action_cost\x18\x04 \x01(\x0b\x32\x0b.Expression\x12\x1c\n\x05goals\x18\x05 \x03(\x0b\x32\r.GoalWithCost\x1a?\n\x10\x41\x63tionCostsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.Expression:\x02\x38\x01\"\xc9\x01\n\nMetricKind\x12\x19\n\x15MINIMIZE_ACTION_COSTS\x10\x00\x12#\n\x1fMINIMIZE_SEQUENTIAL_PLAN_LENGTH\x10\x01\x12\x15\n\x11MINIMIZE_MAKESPAN\x10\x02\x12&\n\"MINIMIZE_EXPRESSION_ON_FINAL_STATE\x10\x03\x12&\n\"MAXIMIZE_EXPRESSION_ON_FINAL_STATE\x10\x04\x12\x14\n\x10OVERSUBSCRIPTION\x10\x05\"\xe2\x02\n\x07Problem\x12\x13\n\x0b\x64omain_name\x18\x01 \x01(\t\x12\x14\n\x0cproblem_name\x18\x02 \x01(\t\x12\x1f\n\x05types\x18\x03 \x03(\x0b\x32\x10.TypeDeclaration\x12\x18\n\x07\x66luents\x18\x04 \x03(\x0b\x32\x07.Fluent\x12#\n\x07objects\x18\x05 \x03(\x0b\x32\x12.ObjectDeclaration\x12\x18\n\x07\x61\x63tions\x18\x06 \x03(\x0b\x32\x07.Action\x12\"\n\rinitial_state\x18\x07 \x03(\x0b\x32\x0b.Assignment\x12#\n\rtimed_effects\x18\x08 \x03(\x0b\x32\x0c.TimedEffect\x12\x14\n\x05goals\x18\t \x03(\x0b\x32\x05.Goal\x12\x1a\n\x08\x66\x65\x61tures\x18\n \x03(\x0e\x32\x08.Feature\x12\x18\n\x07metrics\x18\x0b \x03(\x0b\x32\x07.Metric\x12\x1d\n\thierarchy\x18\x0c \x01(\x0b\x32\n.Hierarchy\"\x80\x01\n\x0e\x41\x63tionInstance\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0b\x61\x63tion_name\x18\x02 \x01(\t\x12\x19\n\nparameters\x18\x03 \x03(\x0b\x32\x05.Atom\x12\x19\n\nstart_time\x18\x04 \x01(\x0b\x32\x05.Real\x12\x17\n\x08\x65nd_time\x18\x05 \x01(\x0b\x32\x05.Real\"(\n\x04Plan\x12 \n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32\x0f.ActionInstance\"\x83\x02\n\x0bPlanRequest\x12\x19\n\x07problem\x18\x01 \x01(\x0b\x32\x08.Problem\x12*\n\x0fresolution_mode\x18\x02 \x01(\x0e\x32\x11.PlanRequest.Mode\x12\x0f\n\x07timeout\x18\x03 \x01(\x01\x12\x37\n\x0e\x65ngine_options\x18\x04 \x03(\x0b\x32\x1f.PlanRequest.EngineOptionsEntry\x1a\x34\n\x12\x45ngineOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"-\n\x04Mode\x12\x0f\n\x0bSATISFIABLE\x10\x00\x12\x14\n\x10SOLVED_OPTIMALLY\x10\x01\"C\n\x11ValidationRequest\x12\x19\n\x07problem\x18\x01 \x01(\x0b\x32\x08.Problem\x12\x13\n\x04plan\x18\x02 \x01(\x0b\x32\x05.Plan\"{\n\nLogMessage\x12#\n\x05level\x18\x01 \x01(\x0e\x32\x14.LogMessage.LogLevel\x12\x0f\n\x07message\x18\x02 \x01(\t\"7\n\x08LogLevel\x12\t\n\x05\x44\x45\x42UG\x10\x00\x12\x08\n\x04INFO\x10\x01\x12\x0b\n\x07WARNING\x10\x02\x12\t\n\x05\x45RROR\x10\x03\"\xbf\x03\n\x14PlanGenerationResult\x12,\n\x06status\x18\x01 \x01(\x0e\x32\x1c.PlanGenerationResult.Status\x12\x13\n\x04plan\x18\x02 \x01(\x0b\x32\x05.Plan\x12\x33\n\x07metrics\x18\x03 \x03(\x0b\x32\".PlanGenerationResult.MetricsEntry\x12!\n\x0clog_messages\x18\x04 \x03(\x0b\x32\x0b.LogMessage\x12\x17\n\x06\x65ngine\x18\x05 \x01(\x0b\x32\x07.Engine\x1a.\n\x0cMetricsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xc2\x01\n\x06Status\x12\x16\n\x12SOLVED_SATISFICING\x10\x00\x12\x14\n\x10SOLVED_OPTIMALLY\x10\x01\x12\x15\n\x11UNSOLVABLE_PROVEN\x10\x02\x12\x1b\n\x17UNSOLVABLE_INCOMPLETELY\x10\x03\x12\x0b\n\x07TIMEOUT\x10\r\x12\n\n\x06MEMOUT\x10\x0e\x12\x12\n\x0eINTERNAL_ERROR\x10\x0f\x12\x17\n\x13UNSUPPORTED_PROBLEM\x10\x10\x12\x10\n\x0cINTERMEDIATE\x10\x11\"\x16\n\x06\x45ngine\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xba\x01\n\x10ValidationResult\x12\x38\n\x06status\x18\x01 \x01(\x0e\x32(.ValidationResult.ValidationResultStatus\x12!\n\x0clog_messages\x18\x02 \x03(\x0b\x32\x0b.LogMessage\x12\x17\n\x06\x65ngine\x18\x03 \x01(\x0b\x32\x07.Engine\"0\n\x16ValidationResultStatus\x12\t\n\x05VALID\x10\x00\x12\x0b\n\x07INVALID\x10\x01\"\xe5\x01\n\x0e\x43ompilerResult\x12\x19\n\x07problem\x18\x01 \x01(\x0b\x32\x08.Problem\x12\x37\n\rmap_back_plan\x18\x02 \x03(\x0b\x32 .CompilerResult.MapBackPlanEntry\x12!\n\x0clog_messages\x18\x03 \x03(\x0b\x32\x0b.LogMessage\x12\x17\n\x06\x65ngine\x18\x04 \x01(\x0b\x32\x07.Engine\x1a\x43\n\x10MapBackPlanEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0f.ActionInstance:\x02\x38\x01*\xb0\x01\n\x0e\x45xpressionKind\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0c\n\x08\x43ONSTANT\x10\x01\x12\r\n\tPARAMETER\x10\x02\x12\x0c\n\x08VARIABLE\x10\x07\x12\x11\n\rFLUENT_SYMBOL\x10\x03\x12\x13\n\x0f\x46UNCTION_SYMBOL\x10\x04\x12\x12\n\x0eSTATE_VARIABLE\x10\x05\x12\x18\n\x14\x46UNCTION_APPLICATION\x10\x06\x12\x10\n\x0c\x43ONTAINER_ID\x10\x08*\xde\x05\n\x07\x46\x65\x61ture\x12\x10\n\x0c\x41\x43TION_BASED\x10\x00\x12\x10\n\x0cHIERARCHICAL\x10\x1a\x12\x1b\n\x17SIMPLE_NUMERIC_PLANNING\x10\x1e\x12\x1c\n\x18GENERAL_NUMERIC_PLANNING\x10\x1f\x12\x13\n\x0f\x43ONTINUOUS_TIME\x10\x01\x12\x11\n\rDISCRETE_TIME\x10\x02\x12\'\n#INTERMEDIATE_CONDITIONS_AND_EFFECTS\x10\x03\x12\x10\n\x0cTIMED_EFFECT\x10\x04\x12\x0f\n\x0bTIMED_GOALS\x10\x05\x12\x19\n\x15\x44URATION_INEQUALITIES\x10\x06\x12\x1e\n\x1aSTATIC_FLUENTS_IN_DURATION\x10\x1b\x12\x17\n\x13\x46LUENTS_IN_DURATION\x10\x1c\x12\x16\n\x12\x43ONTINUOUS_NUMBERS\x10\x07\x12\x14\n\x10\x44ISCRETE_NUMBERS\x10\x08\x12\x17\n\x13NEGATIVE_CONDITIONS\x10\t\x12\x1a\n\x16\x44ISJUNCTIVE_CONDITIONS\x10\n\x12\x0c\n\x08\x45QUALITY\x10\x0b\x12\x1a\n\x16\x45XISTENTIAL_CONDITIONS\x10\x0c\x12\x18\n\x14UNIVERSAL_CONDITIONS\x10\r\x12\x17\n\x13\x43ONDITIONAL_EFFECTS\x10\x0e\x12\x14\n\x10INCREASE_EFFECTS\x10\x0f\x12\x14\n\x10\x44\x45\x43REASE_EFFECTS\x10\x10\x12\x0f\n\x0b\x46LAT_TYPING\x10\x11\x12\x17\n\x13HIERARCHICAL_TYPING\x10\x12\x12\x13\n\x0fNUMERIC_FLUENTS\x10\x13\x12\x12\n\x0eOBJECT_FLUENTS\x10\x14\x12\x10\n\x0c\x41\x43TIONS_COST\x10\x15\x12\x0f\n\x0b\x46INAL_VALUE\x10\x16\x12\x0c\n\x08MAKESPAN\x10\x17\x12\x0f\n\x0bPLAN_LENGTH\x10\x18\x12\x14\n\x10OVERSUBSCRIPTION\x10\x1d\x12\x15\n\x11SIMULATED_EFFECTS\x10\x19\x32\xd8\x01\n\x0fUnifiedPlanning\x12\x34\n\x0bplanAnytime\x12\x0c.PlanRequest\x1a\x15.PlanGenerationResult0\x01\x12\x32\n\x0bplanOneShot\x12\x0c.PlanRequest\x1a\x15.PlanGenerationResult\x12\x35\n\x0cvalidatePlan\x12\x12.ValidationRequest\x1a\x11.ValidationResult\x12$\n\x07\x63ompile\x12\x08.Problem\x1a\x0f.CompilerResultb\x06proto3')

_EXPRESSIONKIND = DESCRIPTOR.enum_types_by_name['ExpressionKind']
ExpressionKind = enum_type_wrapper.EnumTypeWrapper(_EXPRESSIONKIND)
_FEATURE = DESCRIPTOR.enum_types_by_name['Feature']
Feature = enum_type_wrapper.EnumTypeWrapper(_FEATURE)
UNKNOWN = 0
CONSTANT = 1
PARAMETER = 2
VARIABLE = 7
FLUENT_SYMBOL = 3
FUNCTION_SYMBOL = 4
STATE_VARIABLE = 5
FUNCTION_APPLICATION = 6
CONTAINER_ID = 8
ACTION_BASED = 0
HIERARCHICAL = 26
SIMPLE_NUMERIC_PLANNING = 30
GENERAL_NUMERIC_PLANNING = 31
CONTINUOUS_TIME = 1
DISCRETE_TIME = 2
INTERMEDIATE_CONDITIONS_AND_EFFECTS = 3
TIMED_EFFECT = 4
TIMED_GOALS = 5
DURATION_INEQUALITIES = 6
STATIC_FLUENTS_IN_DURATION = 27
FLUENTS_IN_DURATION = 28
CONTINUOUS_NUMBERS = 7
DISCRETE_NUMBERS = 8
NEGATIVE_CONDITIONS = 9
DISJUNCTIVE_CONDITIONS = 10
EQUALITY = 11
EXISTENTIAL_CONDITIONS = 12
UNIVERSAL_CONDITIONS = 13
CONDITIONAL_EFFECTS = 14
INCREASE_EFFECTS = 15
DECREASE_EFFECTS = 16
FLAT_TYPING = 17
HIERARCHICAL_TYPING = 18
NUMERIC_FLUENTS = 19
OBJECT_FLUENTS = 20
ACTIONS_COST = 21
FINAL_VALUE = 22
MAKESPAN = 23
PLAN_LENGTH = 24
OVERSUBSCRIPTION = 29
SIMULATED_EFFECTS = 25


_EXPRESSION = DESCRIPTOR.message_types_by_name['Expression']
_ATOM = DESCRIPTOR.message_types_by_name['Atom']
_REAL = DESCRIPTOR.message_types_by_name['Real']
_TYPEDECLARATION = DESCRIPTOR.message_types_by_name['TypeDeclaration']
_PARAMETER = DESCRIPTOR.message_types_by_name['Parameter']
_FLUENT = DESCRIPTOR.message_types_by_name['Fluent']
_OBJECTDECLARATION = DESCRIPTOR.message_types_by_name['ObjectDeclaration']
_EFFECTEXPRESSION = DESCRIPTOR.message_types_by_name['EffectExpression']
_EFFECT = DESCRIPTOR.message_types_by_name['Effect']
_CONDITION = DESCRIPTOR.message_types_by_name['Condition']
_ACTION = DESCRIPTOR.message_types_by_name['Action']
_TIMEPOINT = DESCRIPTOR.message_types_by_name['Timepoint']
_TIMING = DESCRIPTOR.message_types_by_name['Timing']
_INTERVAL = DESCRIPTOR.message_types_by_name['Interval']
_TIMEINTERVAL = DESCRIPTOR.message_types_by_name['TimeInterval']
_DURATION = DESCRIPTOR.message_types_by_name['Duration']
_ABSTRACTTASKDECLARATION = DESCRIPTOR.message_types_by_name['AbstractTaskDeclaration']
_TASK = DESCRIPTOR.message_types_by_name['Task']
_METHOD = DESCRIPTOR.message_types_by_name['Method']
_TASKNETWORK = DESCRIPTOR.message_types_by_name['TaskNetwork']
_HIERARCHY = DESCRIPTOR.message_types_by_name['Hierarchy']
_GOAL = DESCRIPTOR.message_types_by_name['Goal']
_TIMEDEFFECT = DESCRIPTOR.message_types_by_name['TimedEffect']
_ASSIGNMENT = DESCRIPTOR.message_types_by_name['Assignment']
_GOALWITHCOST = DESCRIPTOR.message_types_by_name['GoalWithCost']
_METRIC = DESCRIPTOR.message_types_by_name['Metric']
_METRIC_ACTIONCOSTSENTRY = _METRIC.nested_types_by_name['ActionCostsEntry']
_PROBLEM = DESCRIPTOR.message_types_by_name['Problem']
_ACTIONINSTANCE = DESCRIPTOR.message_types_by_name['ActionInstance']
_PLAN = DESCRIPTOR.message_types_by_name['Plan']
_PLANREQUEST = DESCRIPTOR.message_types_by_name['PlanRequest']
_PLANREQUEST_ENGINEOPTIONSENTRY = _PLANREQUEST.nested_types_by_name['EngineOptionsEntry']
_VALIDATIONREQUEST = DESCRIPTOR.message_types_by_name['ValidationRequest']
_LOGMESSAGE = DESCRIPTOR.message_types_by_name['LogMessage']
_PLANGENERATIONRESULT = DESCRIPTOR.message_types_by_name['PlanGenerationResult']
_PLANGENERATIONRESULT_METRICSENTRY = _PLANGENERATIONRESULT.nested_types_by_name['MetricsEntry']
_ENGINE = DESCRIPTOR.message_types_by_name['Engine']
_VALIDATIONRESULT = DESCRIPTOR.message_types_by_name['ValidationResult']
_COMPILERRESULT = DESCRIPTOR.message_types_by_name['CompilerResult']
_COMPILERRESULT_MAPBACKPLANENTRY = _COMPILERRESULT.nested_types_by_name['MapBackPlanEntry']
_EFFECTEXPRESSION_EFFECTKIND = _EFFECTEXPRESSION.enum_types_by_name['EffectKind']
_TIMEPOINT_TIMEPOINTKIND = _TIMEPOINT.enum_types_by_name['TimepointKind']
_METRIC_METRICKIND = _METRIC.enum_types_by_name['MetricKind']
_PLANREQUEST_MODE = _PLANREQUEST.enum_types_by_name['Mode']
_LOGMESSAGE_LOGLEVEL = _LOGMESSAGE.enum_types_by_name['LogLevel']
_PLANGENERATIONRESULT_STATUS = _PLANGENERATIONRESULT.enum_types_by_name['Status']
_VALIDATIONRESULT_VALIDATIONRESULTSTATUS = _VALIDATIONRESULT.enum_types_by_name['ValidationResultStatus']
Expression = _reflection.GeneratedProtocolMessageType('Expression', (_message.Message,), {
  'DESCRIPTOR' : _EXPRESSION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Expression)
  })
_sym_db.RegisterMessage(Expression)

Atom = _reflection.GeneratedProtocolMessageType('Atom', (_message.Message,), {
  'DESCRIPTOR' : _ATOM,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Atom)
  })
_sym_db.RegisterMessage(Atom)

Real = _reflection.GeneratedProtocolMessageType('Real', (_message.Message,), {
  'DESCRIPTOR' : _REAL,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Real)
  })
_sym_db.RegisterMessage(Real)

TypeDeclaration = _reflection.GeneratedProtocolMessageType('TypeDeclaration', (_message.Message,), {
  'DESCRIPTOR' : _TYPEDECLARATION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:TypeDeclaration)
  })
_sym_db.RegisterMessage(TypeDeclaration)

Parameter = _reflection.GeneratedProtocolMessageType('Parameter', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETER,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Parameter)
  })
_sym_db.RegisterMessage(Parameter)

Fluent = _reflection.GeneratedProtocolMessageType('Fluent', (_message.Message,), {
  'DESCRIPTOR' : _FLUENT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Fluent)
  })
_sym_db.RegisterMessage(Fluent)

ObjectDeclaration = _reflection.GeneratedProtocolMessageType('ObjectDeclaration', (_message.Message,), {
  'DESCRIPTOR' : _OBJECTDECLARATION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:ObjectDeclaration)
  })
_sym_db.RegisterMessage(ObjectDeclaration)

EffectExpression = _reflection.GeneratedProtocolMessageType('EffectExpression', (_message.Message,), {
  'DESCRIPTOR' : _EFFECTEXPRESSION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:EffectExpression)
  })
_sym_db.RegisterMessage(EffectExpression)

Effect = _reflection.GeneratedProtocolMessageType('Effect', (_message.Message,), {
  'DESCRIPTOR' : _EFFECT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Effect)
  })
_sym_db.RegisterMessage(Effect)

Condition = _reflection.GeneratedProtocolMessageType('Condition', (_message.Message,), {
  'DESCRIPTOR' : _CONDITION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Condition)
  })
_sym_db.RegisterMessage(Condition)

Action = _reflection.GeneratedProtocolMessageType('Action', (_message.Message,), {
  'DESCRIPTOR' : _ACTION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Action)
  })
_sym_db.RegisterMessage(Action)

Timepoint = _reflection.GeneratedProtocolMessageType('Timepoint', (_message.Message,), {
  'DESCRIPTOR' : _TIMEPOINT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Timepoint)
  })
_sym_db.RegisterMessage(Timepoint)

Timing = _reflection.GeneratedProtocolMessageType('Timing', (_message.Message,), {
  'DESCRIPTOR' : _TIMING,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Timing)
  })
_sym_db.RegisterMessage(Timing)

Interval = _reflection.GeneratedProtocolMessageType('Interval', (_message.Message,), {
  'DESCRIPTOR' : _INTERVAL,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Interval)
  })
_sym_db.RegisterMessage(Interval)

TimeInterval = _reflection.GeneratedProtocolMessageType('TimeInterval', (_message.Message,), {
  'DESCRIPTOR' : _TIMEINTERVAL,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:TimeInterval)
  })
_sym_db.RegisterMessage(TimeInterval)

Duration = _reflection.GeneratedProtocolMessageType('Duration', (_message.Message,), {
  'DESCRIPTOR' : _DURATION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Duration)
  })
_sym_db.RegisterMessage(Duration)

AbstractTaskDeclaration = _reflection.GeneratedProtocolMessageType('AbstractTaskDeclaration', (_message.Message,), {
  'DESCRIPTOR' : _ABSTRACTTASKDECLARATION,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:AbstractTaskDeclaration)
  })
_sym_db.RegisterMessage(AbstractTaskDeclaration)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Task)
  })
_sym_db.RegisterMessage(Task)

Method = _reflection.GeneratedProtocolMessageType('Method', (_message.Message,), {
  'DESCRIPTOR' : _METHOD,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Method)
  })
_sym_db.RegisterMessage(Method)

TaskNetwork = _reflection.GeneratedProtocolMessageType('TaskNetwork', (_message.Message,), {
  'DESCRIPTOR' : _TASKNETWORK,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:TaskNetwork)
  })
_sym_db.RegisterMessage(TaskNetwork)

Hierarchy = _reflection.GeneratedProtocolMessageType('Hierarchy', (_message.Message,), {
  'DESCRIPTOR' : _HIERARCHY,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Hierarchy)
  })
_sym_db.RegisterMessage(Hierarchy)

Goal = _reflection.GeneratedProtocolMessageType('Goal', (_message.Message,), {
  'DESCRIPTOR' : _GOAL,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Goal)
  })
_sym_db.RegisterMessage(Goal)

TimedEffect = _reflection.GeneratedProtocolMessageType('TimedEffect', (_message.Message,), {
  'DESCRIPTOR' : _TIMEDEFFECT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:TimedEffect)
  })
_sym_db.RegisterMessage(TimedEffect)

Assignment = _reflection.GeneratedProtocolMessageType('Assignment', (_message.Message,), {
  'DESCRIPTOR' : _ASSIGNMENT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Assignment)
  })
_sym_db.RegisterMessage(Assignment)

GoalWithCost = _reflection.GeneratedProtocolMessageType('GoalWithCost', (_message.Message,), {
  'DESCRIPTOR' : _GOALWITHCOST,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:GoalWithCost)
  })
_sym_db.RegisterMessage(GoalWithCost)

Metric = _reflection.GeneratedProtocolMessageType('Metric', (_message.Message,), {

  'ActionCostsEntry' : _reflection.GeneratedProtocolMessageType('ActionCostsEntry', (_message.Message,), {
    'DESCRIPTOR' : _METRIC_ACTIONCOSTSENTRY,
    '__module__' : 'unified_planning_pb2'
    # @@protoc_insertion_point(class_scope:Metric.ActionCostsEntry)
    })
  ,
  'DESCRIPTOR' : _METRIC,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Metric)
  })
_sym_db.RegisterMessage(Metric)
_sym_db.RegisterMessage(Metric.ActionCostsEntry)

Problem = _reflection.GeneratedProtocolMessageType('Problem', (_message.Message,), {
  'DESCRIPTOR' : _PROBLEM,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Problem)
  })
_sym_db.RegisterMessage(Problem)

ActionInstance = _reflection.GeneratedProtocolMessageType('ActionInstance', (_message.Message,), {
  'DESCRIPTOR' : _ACTIONINSTANCE,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:ActionInstance)
  })
_sym_db.RegisterMessage(ActionInstance)

Plan = _reflection.GeneratedProtocolMessageType('Plan', (_message.Message,), {
  'DESCRIPTOR' : _PLAN,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Plan)
  })
_sym_db.RegisterMessage(Plan)

PlanRequest = _reflection.GeneratedProtocolMessageType('PlanRequest', (_message.Message,), {

  'EngineOptionsEntry' : _reflection.GeneratedProtocolMessageType('EngineOptionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _PLANREQUEST_ENGINEOPTIONSENTRY,
    '__module__' : 'unified_planning_pb2'
    # @@protoc_insertion_point(class_scope:PlanRequest.EngineOptionsEntry)
    })
  ,
  'DESCRIPTOR' : _PLANREQUEST,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:PlanRequest)
  })
_sym_db.RegisterMessage(PlanRequest)
_sym_db.RegisterMessage(PlanRequest.EngineOptionsEntry)

ValidationRequest = _reflection.GeneratedProtocolMessageType('ValidationRequest', (_message.Message,), {
  'DESCRIPTOR' : _VALIDATIONREQUEST,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:ValidationRequest)
  })
_sym_db.RegisterMessage(ValidationRequest)

LogMessage = _reflection.GeneratedProtocolMessageType('LogMessage', (_message.Message,), {
  'DESCRIPTOR' : _LOGMESSAGE,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:LogMessage)
  })
_sym_db.RegisterMessage(LogMessage)

PlanGenerationResult = _reflection.GeneratedProtocolMessageType('PlanGenerationResult', (_message.Message,), {

  'MetricsEntry' : _reflection.GeneratedProtocolMessageType('MetricsEntry', (_message.Message,), {
    'DESCRIPTOR' : _PLANGENERATIONRESULT_METRICSENTRY,
    '__module__' : 'unified_planning_pb2'
    # @@protoc_insertion_point(class_scope:PlanGenerationResult.MetricsEntry)
    })
  ,
  'DESCRIPTOR' : _PLANGENERATIONRESULT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:PlanGenerationResult)
  })
_sym_db.RegisterMessage(PlanGenerationResult)
_sym_db.RegisterMessage(PlanGenerationResult.MetricsEntry)

Engine = _reflection.GeneratedProtocolMessageType('Engine', (_message.Message,), {
  'DESCRIPTOR' : _ENGINE,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:Engine)
  })
_sym_db.RegisterMessage(Engine)

ValidationResult = _reflection.GeneratedProtocolMessageType('ValidationResult', (_message.Message,), {
  'DESCRIPTOR' : _VALIDATIONRESULT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:ValidationResult)
  })
_sym_db.RegisterMessage(ValidationResult)

CompilerResult = _reflection.GeneratedProtocolMessageType('CompilerResult', (_message.Message,), {

  'MapBackPlanEntry' : _reflection.GeneratedProtocolMessageType('MapBackPlanEntry', (_message.Message,), {
    'DESCRIPTOR' : _COMPILERRESULT_MAPBACKPLANENTRY,
    '__module__' : 'unified_planning_pb2'
    # @@protoc_insertion_point(class_scope:CompilerResult.MapBackPlanEntry)
    })
  ,
  'DESCRIPTOR' : _COMPILERRESULT,
  '__module__' : 'unified_planning_pb2'
  # @@protoc_insertion_point(class_scope:CompilerResult)
  })
_sym_db.RegisterMessage(CompilerResult)
_sym_db.RegisterMessage(CompilerResult.MapBackPlanEntry)

_UNIFIEDPLANNING = DESCRIPTOR.services_by_name['UnifiedPlanning']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _METRIC_ACTIONCOSTSENTRY._options = None
  _METRIC_ACTIONCOSTSENTRY._serialized_options = b'8\001'
  _PLANREQUEST_ENGINEOPTIONSENTRY._options = None
  _PLANREQUEST_ENGINEOPTIONSENTRY._serialized_options = b'8\001'
  _PLANGENERATIONRESULT_METRICSENTRY._options = None
  _PLANGENERATIONRESULT_METRICSENTRY._serialized_options = b'8\001'
  _COMPILERRESULT_MAPBACKPLANENTRY._options = None
  _COMPILERRESULT_MAPBACKPLANENTRY._serialized_options = b'8\001'
  _EXPRESSIONKIND._serialized_start=4719
  _EXPRESSIONKIND._serialized_end=4895
  _FEATURE._serialized_start=4898
  _FEATURE._serialized_end=5632
  _EXPRESSION._serialized_start=26
  _EXPRESSION._serialized_end=131
  _ATOM._serialized_start=133
  _ATOM._serialized_end=225
  _REAL._serialized_start=227
  _REAL._serialized_end=273
  _TYPEDECLARATION._serialized_start=275
  _TYPEDECLARATION._serialized_end=332
  _PARAMETER._serialized_start=334
  _PARAMETER._serialized_end=373
  _FLUENT._serialized_start=375
  _FLUENT._serialized_end=485
  _OBJECTDECLARATION._serialized_start=487
  _OBJECTDECLARATION._serialized_end=534
  _EFFECTEXPRESSION._serialized_start=537
  _EFFECTEXPRESSION._serialized_end=742
  _EFFECTEXPRESSION_EFFECTKIND._serialized_start=690
  _EFFECTEXPRESSION_EFFECTKIND._serialized_end=742
  _EFFECT._serialized_start=744
  _EFFECT._serialized_end=821
  _CONDITION._serialized_start=823
  _CONDITION._serialized_end=890
  _ACTION._serialized_start=893
  _ACTION._serialized_end=1034
  _TIMEPOINT._serialized_start=1037
  _TIMEPOINT._serialized_end=1181
  _TIMEPOINT_TIMEPOINTKIND._serialized_start=1112
  _TIMEPOINT_TIMEPOINTKIND._serialized_end=1181
  _TIMING._serialized_start=1183
  _TIMING._serialized_end=1244
  _INTERVAL._serialized_start=1246
  _INTERVAL._serialized_end=1357
  _TIMEINTERVAL._serialized_start=1359
  _TIMEINTERVAL._serialized_end=1466
  _DURATION._serialized_start=1468
  _DURATION._serialized_end=1521
  _ABSTRACTTASKDECLARATION._serialized_start=1523
  _ABSTRACTTASKDECLARATION._serialized_end=1594
  _TASK._serialized_start=1596
  _TASK._serialized_end=1666
  _METHOD._serialized_start=1669
  _METHOD._serialized_end=1844
  _TASKNETWORK._serialized_start=1846
  _TASKNETWORK._serialized_end=1949
  _HIERARCHY._serialized_start=1952
  _HIERARCHY._serialized_end=2083
  _GOAL._serialized_start=2085
  _GOAL._serialized_end=2149
  _TIMEDEFFECT._serialized_start=2151
  _TIMEDEFFECT._serialized_end=2233
  _ASSIGNMENT._serialized_start=2235
  _ASSIGNMENT._serialized_end=2304
  _GOALWITHCOST._serialized_start=2306
  _GOALWITHCOST._serialized_end=2368
  _METRIC._serialized_start=2371
  _METRIC._serialized_end=2835
  _METRIC_ACTIONCOSTSENTRY._serialized_start=2568
  _METRIC_ACTIONCOSTSENTRY._serialized_end=2631
  _METRIC_METRICKIND._serialized_start=2634
  _METRIC_METRICKIND._serialized_end=2835
  _PROBLEM._serialized_start=2838
  _PROBLEM._serialized_end=3192
  _ACTIONINSTANCE._serialized_start=3195
  _ACTIONINSTANCE._serialized_end=3323
  _PLAN._serialized_start=3325
  _PLAN._serialized_end=3365
  _PLANREQUEST._serialized_start=3368
  _PLANREQUEST._serialized_end=3627
  _PLANREQUEST_ENGINEOPTIONSENTRY._serialized_start=3528
  _PLANREQUEST_ENGINEOPTIONSENTRY._serialized_end=3580
  _PLANREQUEST_MODE._serialized_start=3582
  _PLANREQUEST_MODE._serialized_end=3627
  _VALIDATIONREQUEST._serialized_start=3629
  _VALIDATIONREQUEST._serialized_end=3696
  _LOGMESSAGE._serialized_start=3698
  _LOGMESSAGE._serialized_end=3821
  _LOGMESSAGE_LOGLEVEL._serialized_start=3766
  _LOGMESSAGE_LOGLEVEL._serialized_end=3821
  _PLANGENERATIONRESULT._serialized_start=3824
  _PLANGENERATIONRESULT._serialized_end=4271
  _PLANGENERATIONRESULT_METRICSENTRY._serialized_start=4028
  _PLANGENERATIONRESULT_METRICSENTRY._serialized_end=4074
  _PLANGENERATIONRESULT_STATUS._serialized_start=4077
  _PLANGENERATIONRESULT_STATUS._serialized_end=4271
  _ENGINE._serialized_start=4273
  _ENGINE._serialized_end=4295
  _VALIDATIONRESULT._serialized_start=4298
  _VALIDATIONRESULT._serialized_end=4484
  _VALIDATIONRESULT_VALIDATIONRESULTSTATUS._serialized_start=4436
  _VALIDATIONRESULT_VALIDATIONRESULTSTATUS._serialized_end=4484
  _COMPILERRESULT._serialized_start=4487
  _COMPILERRESULT._serialized_end=4716
  _COMPILERRESULT_MAPBACKPLANENTRY._serialized_start=4649
  _COMPILERRESULT_MAPBACKPLANENTRY._serialized_end=4716
  _UNIFIEDPLANNING._serialized_start=5635
  _UNIFIEDPLANNING._serialized_end=5851
# @@protoc_insertion_point(module_scope)
