from .class_subscription import *

import database as _database
import database_layering as _database_layering

class ClassSubscriptionsListDatabaseTable(_database_layering.DatabaseAssociativeTableFacade[int, int]):
    def get_subscription(self, account: int, nooble_class: int) -> ClassSubscriptionDatabaseElement:
        return ClassSubscriptionDatabaseElement(self.get_table().get_element(account, nooble_class))
    
    def delete_section(self, account: int, nooble_class: int) -> None:
        self.get_table().delete_element(self.get_subscription(account, nooble_class).get_element())

    def get_account_subscriptions(self, account: int, teaching: bool | None = None) -> list[ClassSubscriptionDatabaseElement]:
        if teaching is None:
            elements = self.get_table().find_elements_with_clause(
                _database.SQLColumn('class'), 
                _database.SQLClauseWhere(
                    _database.SQLOpEquality(_database.SQLColumn('account'), _database.SQLInteger(account))
                )
            )
        else:
            elements = self.get_table().find_elements_with_clause(
                _database.SQLColumn('class'), 
                _database.SQLClauseWhere(
                    _database.SQLOpAnd(
                        _database.SQLOpEquality(_database.SQLColumn('account'), _database.SQLInteger(account)),
                        _database.SQLOpEquality(_database.SQLColumn('as_teacher'), _database.SQLBool(teaching)),
                    )
                )
            )

        return [ClassSubscriptionDatabaseElement(element) for element in elements]

    def get_class_subscriptions(self, class_id: int, teaching: bool | None = None) -> list[ClassSubscriptionDatabaseElement]:
        if teaching is None:
            elements = self.get_table().find_elements_with_clause(
                _database.SQLColumn('account'), 
                _database.SQLClauseWhere(
                    _database.SQLOpEquality(_database.SQLColumn('class'), _database.SQLInteger(class_id))
                )
            )
        else:
            elements = self.get_table().find_elements_with_clause(
                _database.SQLColumn('account'), 
                _database.SQLClauseWhere(
                    _database.SQLOpAnd(
                        _database.SQLOpEquality(_database.SQLColumn('class'), _database.SQLInteger(class_id)),
                        _database.SQLOpEquality(_database.SQLColumn('as_teacher'), _database.SQLBool(teaching)),
                    )
                )
            )
        return [ClassSubscriptionDatabaseElement(element) for element in elements]




