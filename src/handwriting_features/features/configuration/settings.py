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

        # Number of intra-stroke intersections
        "number_of_intra_stroke_intersections": {
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

        # Relative number of intra-stroke intersections
        "relative_number_of_intra_stroke_intersections": {
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

        # Total number of intra-stroke intersections
        "total_number_of_intra_stroke_intersections": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Relative total number of intra-stroke intersections
        "relative_total_number_of_intra_stroke_intersections": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Number of inter-stroke intersections
        "number_of_inter_stroke_intersections": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Relative number of inter-stroke intersections
        "relative_number_of_inter_stroke_intersections": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {}
        },

        # Vertical peaks indices
        "vertical_peaks_indices": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical valleys indices
        "vertical_valleys_indices": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical peaks values
        "vertical_peaks_values": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical valleys values
        "vertical_valleys_values": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical peaks velocity
        "vertical_peaks_velocity": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical valleys velocity
        "vertical_valleys_velocity": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical peaks distance
        "vertical_peaks_distance": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical valleys distance
        "vertical_valleys_distance": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical peaks duration
        "vertical_peaks_duration": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
                }
            }
        },

        # Vertical valleys duration
        "vertical_valleys_duration": {
            "properties": {
                "is_multi_valued": True
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                },
                "statistics": {
                    "mandatory": False,
                    "type": [str, list, tuple],
                    "options": statistics
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

        # Number of changes in x profile
        "number_of_changes_in_x_profile": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Number of changes in y profile
        "number_of_changes_in_y_profile": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Number of changes in azimuth
        "number_of_changes_in_azimuth": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Number of changes in tilt
        "number_of_changes_in_tilt": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Number of changes in pressure
        "number_of_changes_in_pressure": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Number of changes in velocity profile
        "number_of_changes_in_velocity_profile": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Relative number of changes in x profile
        "relative_number_of_changes_in_x_profile": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Relative number of changes in y profile
        "relative_number_of_changes_in_y_profile": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Relative number of changes in azimuth
        "relative_number_of_changes_in_azimuth": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Relative number of changes in tilt
        "relative_number_of_changes_in_tilt": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Relative number of changes in pressure
        "relative_number_of_changes_in_pressure": {
            "properties": {
                "is_multi_valued": False
            },
            "arguments": {
                "fs": {
                    "mandatory": True,
                    "type": [int, float]
                }
            }
        },

        # Relative number of changes in velocity profile
        "relative_number_of_changes_in_velocity_profile": {
            "properties": {
                "is_multi_valued": False
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
    def get_feature_arguments(cls, feature_name):
        """
        Gets the feature's arguments.

        :param feature_name: feature name
        :type feature_name: str
        :return: arguments
        :rtype: iterable
        """
        return cls.settings.get(feature_name, {}).get("arguments", {})

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

    @classmethod
    def is_feature_multivalued(cls, feature_name):
        """
        Checks if the feature is multivalued.

        :param feature_name: feature name
        :type feature_name: str
        :return: True if the feature is multivalued, False otherwise
        :rtype: bool
        """
        return cls.settings.get(feature_name, {}).get("properties", {}).get("is_multi_valued", False)
