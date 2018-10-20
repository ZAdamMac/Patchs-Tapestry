#! /usr/bin/python3.6
# Unit tests relating to Tapestry. Current as of 2.0.
# See the documentation - there are dependencies

# Import Block
from datetime import date
from Development.Source import dev
from Development.Testing import framework as fw

# Extra Classes Go Here

# Define Tests As Functions Here


def establish_namespace():
    """This function is best thought of as a general purpose config block and
    returns an object best thought of as a namespace object, used for ferrying
    configuration values around the program.
    """
    ns = type('', (), {})()  # We need a general-purpose namespace object
    ns.key_sign_fp = 0  # TODO input
    ns.key_crypt_fp = 0  # TODO input
    ns.goodRIFF = 0  # TODO Generate and Encode
    ns.filename = "unit_test-" + str(ns.uid) + "-" + str(date.today()) + ".log"
    ns.logger = fw.simpleLogger("Logs", ns.filename, "unit-tests")

    return ns

def test_config_compliance(namespace):
    """Imports /Development/Source/Tapestry.cfg and parses it, then ensures
    that all the expected values are present. This test must be modified after
    development of the release is believed "finished" to ensure all values are
    present and correct.
    """
    pass

def test_encryption_cyclic(namespace):
    """Test the encryption and decryption functions by providing a bytestream
    which acts as a dummy file. The input and output are compared."""
    pass


def test_riff_compliance(namespace):
    """This test compares the known-good RIFF (namespace.goodRIFF) to an RIFF
        generated by the runtime tests and extracted in the integrity test
        script to a known-correct position.
    """
    pass

def test_verification_good(namespace):
    """Tests signing/verification against a bytes object, expecting a valid
    result.
    """
    pass

def test_verification_bad(namespace):
    """Passes a known-badly-signed bytes object into the verification function to
    ensure that the function works as designed. This was necessary to prevent a
    recurrence of the verification bypass bug.
    """
    pass
