from comicsdb.management.commands._utils import clean_description


def test_clean_desciption_teen_plus():
    test_desc = "The moment REED RICHARDS…PEIACOLYPSE?!  Rated T+"
    expected_result = "The moment REED RICHARDS…PEIACOLYPSE?!"

    result = clean_description(test_desc)
    assert expected_result == result


def test_clean_description_teen():
    test_desc = "THE CLONE SAGA - MILES MORALES-STYLE! We finally see the full extent of what the Assessor did when he kidnapped Miles back in #7. This oversized anniversary issue lets the clones loose in Brooklyn and messes with Miles life even more than Peter Parker's Clone Saga messed HIS life up.  Rated T"
    expected_result = "THE CLONE SAGA - MILES MORALES-STYLE! We finally see the full extent of what the Assessor did when he kidnapped Miles back in #7. This oversized anniversary issue lets the clones loose in Brooklyn and messes with Miles life even more than Peter Parker's Clone Saga messed HIS life up."

    result = clean_description(test_desc)
    assert expected_result == result


def test_clean_description_parental():
    test_desc = "A marvelous Marvel team-up between Conan and the Rhino goes awry when Spider-Man threatens to ruin their good time.  Parental Advisory"
    expected_result = "A marvelous Marvel team-up between Conan and the Rhino goes awry when Spider-Man threatens to ruin their good time."
    result = clean_description(test_desc)
    assert expected_result == result
