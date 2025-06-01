import clsx from "clsx";
import React, {type ReactNode} from "react";

const Card = ({children, title, url, full = false, innerPadding = true}: {
    children: ReactNode;
    title?: string;
    url?: string;
    full: boolean;
    innerPadding?: boolean;
}) => {
    return (
        <div
            className={clsx("overflow-hidden flex flex-col rounded shadow bg-white mx-auto w-[min-content]", full && "w-full h-[100%]")}>
            {title && (
                <div
                    className="border-b-[1px] border-gray-200 border-dashed px-6 py-4 flex justify-between items-center">
                    <h2>{title}</h2>
                    {url &&
                        <a href={url} className="button-primary" download={"raport.pdf"} target="_blank">
                            Pokaż raport
                        </a>
                    }
                </div>
            )}
            <div className={clsx("h-full", innerPadding && "p-6")}>{children}</div>
        </div>
    );
};

export default Card;
