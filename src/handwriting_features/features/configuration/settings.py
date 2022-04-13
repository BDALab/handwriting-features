from handwriting_features.data.containers.sample import HandwritingSampleWrapper
from handwriting_features.data.descriptors.statistics import Statistics


class HandwritingFeaturesSettings(object):
    """Class implementing the handwriting features settings"""

    # Handwriting data axes
    axes = HandwritingSampleWrapper.axes

    # Handwriting features statistics
    statistics = Statistics.mapping.keys()

    # Handwriting features settings
    settings = {

        # ---------------------
        # 1. Kinematic features

        # Velocity
        "velocity": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "axis": {
                    "mandatory": False,
                    "type": [str],
                    "options": axes,
                    "default": "xy"
                },
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Acceleration
        "acceleration": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "axis": {
                    "mandatory": False,
                    "type": [str],
                    "options": axes,
                    "default": "xy"
                },
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Jerk
        "jerk": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "axis": {
                    "mandatory": False,
                    "type": [str],
                    "options": axes,
                    "default": "xy"
                },
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # -------------------
        # 2. Dynamic features

        # Azimuth
        "azimuth": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Tilt
        "tilt": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Pressure
        "pressure": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # -------------------
        # 3. Spatial features

        # Stroke length
        "stroke_length": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Stroke height
        "stroke_height": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Stroke width
        "stroke_width": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Writing length
        "writing_length": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                }
            }
        },

        # Writing height
        "writing_height": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                }
            }
        },

        # Writing width
        "writing_width": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                }
            }
        },

        # --------------------
        # 4. Temporal features

        # Stroke duration
        "stroke_duration": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Ratio of stroke durations
        "ratio_of_stroke_durations": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Writing duration
        "writing_duration": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                }
            }
        },

        # Writing duration overall
        "writing_duration_overall": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Ratio of writing durations
        "ratio_of_writing_durations": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Number of interruptions
        "number_of_interruptions": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Number of interruptions relative to the duration
        "number_of_interruptions_relative": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # ---------------------
        # 5. Composite features

        # Writing tempo
        "writing_tempo": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "in_air": {
                    "mandatory": False,
                    "type": [bool],
                    "options": (True, False),
                    "default": False
                }
            }
        },

        # Writing stops
        "writing_stops": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Writing number of changes
        "writing_number_of_changes": {
            "properties": {
                "is_multi_valued": False,
                "is_composite": True,
                "composite_feature_names": [
                    "number_of_changes_in_x_profile",
                    "number_of_changes_in_y_profile",
                    "number_of_changes_in_azimuth",
                    "number_of_changes_in_tilt",
                    "number_of_changes_in_pressure",
                    "number_of_changes_in_velocity",
                    "relative_number_of_changes_in_x_profile",
                    "relative_number_of_changes_in_y_profile",
                    "relative_number_of_changes_in_azimuth",
                    "relative_number_of_changes_in_tilt",
                    "relative_number_of_changes_in_pressure",
                    "relative_number_of_changes_in_velocity"
                ]
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        }
    }

    @classmethod
    def get_feature_argument_type(cls, feature_name, argument_name):
        """
        Gets the feature argument's supported type(s).

        :param feature_name: feature name
        :type feature_name: str
        :param argument_name: argument name
        :type argument_name: str
        :return: argument's type(s)
        :rtype: iterable
        """
        return cls.settings.get(feature_name, {}).get("arguments").get(argument_name, {}).get("type", [])

    @classmethod
    def get_feature_argument_options(cls, feature_name, argument_name):
        """
        Gets the feature argument's option(s).

        :param feature_name: feature name
        :type feature_name: str
        :param argument_name: argument name
        :type argument_name: str
        :return: argument's option(s)
        :rtype: iterable
        """
        return cls.settings.get(feature_name, {}).get("arguments").get(argument_name, {}).get("options", [])

    @classmethod
    def get_feature_argument_default(cls, feature_name, argument_name):
        """
        Gets the feature argument's default value(s).

        :param feature_name: feature name
        :type feature_name: str
        :param argument_name: argument name
        :type argument_name: str
        :return: argument's default value(s)
        :rtype: Any
        """
        return cls.settings.get(feature_name, {}).get("arguments").get(argument_name, {}).get("default")
